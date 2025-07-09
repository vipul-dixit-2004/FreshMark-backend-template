import pandas as pd
import joblib
import os
import numpy as np

# Define model folder path
MODEL_DIR = "models"

# Load model
MODEL_PATH = os.path.join(MODEL_DIR, "walmart_model.pkl")
model = joblib.load(MODEL_PATH)

# Load maps from the same folder
category_map = joblib.load(os.path.join(MODEL_DIR, "category_map.pkl"))
category_avg_price_map = joblib.load(os.path.join(MODEL_DIR, "category_avg_price_map.pkl"))
supplier_freq_map = joblib.load(os.path.join(MODEL_DIR, "supplier_freq_map.pkl"))


REQUIRED_FEATURES = [
    'Unit_Price',
    'Days_Until_Expiry',
    'Stock_Quantity',
    'Inventory_Turnover_Rate',
    'Stock_Urgency',
    'Expiry_Urgency',
    'Urgency_Combined',
    'Stock_Per_Expiry_Day',
    'Category_Encoded',
    'Days_Since_Last_Order',
    'Category_Avg_Price',
    'Supplier_Reorder_Freq',
    'Sales_Volume',
    'Reorder_Level',
    'Reorder_Quantity',
    'Price_Per_Unit_Inventory',
    'Turnover_Per_Day'
]

def predict_price(raw_input_data):
    try:
        # Step 1: Derive all required features from the raw input
        df = prepare_features_from_input(
            raw_input_data,
            category_map,
            supplier_freq_map,
            category_avg_price_map
        )

        # Step 2: Validate required features exist
        for feat in REQUIRED_FEATURES:
            if feat not in df.columns:
                return {'error': f'Missing required feature: {feat}'}

        # Step 3: Predict
        prediction = model.predict(df)[0]
        return {'predicted_dynamic_price': round(float(prediction), 2)}
    
    except Exception as e:
        return {'error': str(e)}



def prepare_features_from_input(json_input, category_map, supplier_freq_map, category_avg_price_map):
    # Convert to DataFrame
    df = pd.DataFrame([json_input])
    
    # Convert dates
    df['Date_Received'] = pd.to_datetime(df['Date_Received'])
    df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])
    df['Last_Order_Date'] = pd.to_datetime(df['Last_Order_Date'])

    # Derived features
    df['Days_Until_Expiry'] = (df['Expiration_Date'] - df['Date_Received']).dt.days
    df['Days_Since_Last_Order'] = (df['Date_Received'] - df['Last_Order_Date']).dt.days
    df['Stock_Urgency'] = np.where(df['Stock_Quantity'] <= df['Reorder_Level'], 1, 0)
    df['Expiry_Urgency'] = np.where(df['Days_Until_Expiry'] <= 3, 1, 0)
    df['Urgency_Combined'] = df['Stock_Urgency'] + df['Expiry_Urgency']
    df['Stock_Per_Expiry_Day'] = df['Stock_Quantity'] / (df['Days_Until_Expiry'] + 1)
    df['Price_Per_Unit_Inventory'] = df['Unit_Price'] / (df['Stock_Quantity'] + 1)
    df['Turnover_Per_Day'] = df['Inventory_Turnover_Rate'] / (df['Days_Until_Expiry'] + 1)

    # Encoded features with fallback
    df['Category_Encoded'] = df['Category'].map(category_map).fillna(-1).astype(int)
    df['Category_Avg_Price'] = df['Category'].map(category_avg_price_map).fillna(df['Unit_Price'].mean())
    df['Supplier_Reorder_Freq'] = df['Supplier_ID'].map(supplier_freq_map).fillna(df['Reorder_Quantity'].mean())

    return df[REQUIRED_FEATURES]
