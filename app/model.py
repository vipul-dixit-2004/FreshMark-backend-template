import pandas as pd
import joblib
import os

MODEL_PATH = os.path.join("models", "walmart_model.pkl")
model = joblib.load(MODEL_PATH)

REQUIRED_FEATURES = [
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

def predict_price(data):
    df = pd.DataFrame([data])

    for feat in REQUIRED_FEATURES:
        if feat not in df.columns:
            return {'error': f'Missing required feature: {feat}'}

    df = df[REQUIRED_FEATURES]
    prediction = model.predict(df)[0]
    return {'predicted_dynamic_price': round(float(prediction), 2)}
