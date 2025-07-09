import requests

sample_data = {
    "Unit_Price": 12.99,
    "Stock_Quantity": 80,
    "Reorder_Level": 60,
    "Inventory_Turnover_Rate": 1.5,
    "Sales_Volume": 200,
    "Reorder_Quantity": 120,
    "Category": "Dairy",
    "Supplier_ID": "SUPP123",
    "Date_Received": "2025-07-09",
    "Expiration_Date": "2025-07-12",
    "Last_Order_Date": "2025-06-30"
}

response = requests.post("http://localhost:5000/predict", json=sample_data)
print(response.json())