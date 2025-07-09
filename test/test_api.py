import requests

sample_data = {
    "Days_Until_Expiry": 30,
    "Stock_Quantity": 100,
    "Inventory_Turnover_Rate": 1.5,
    "Stock_Urgency": 2,
    "Expiry_Urgency": 1,
    "Urgency_Combined": 3,
    "Stock_Per_Expiry_Day": 3.3,
    "Category_Encoded": 2,
    "Days_Since_Last_Order": 5,
    "Category_Avg_Price": 12.5,
    "Supplier_Reorder_Freq": 10,
    "Sales_Volume": 500,
    "Reorder_Level": 50,
    "Reorder_Quantity": 70,
    "Price_Per_Unit_Inventory": 10.5,
    "Turnover_Per_Day": 0.15
}

response = requests.post("http://localhost:5000/predict", json=sample_data)
print(response.json())