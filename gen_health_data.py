import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- SETTINGS ---
rows = 2000 # 2,000 transactions

# --- HEALTHCARE CATEGORIES ---
items = {
    'Medical Consumables': [
        ('Nitrile Gloves (Box)', 12.50), 
        ('N95 Masks (Pack)', 25.00), 
        ('IV Tubing Set', 4.20), 
        ('Syringes 5ml (Box)', 8.50)
    ],
    'Facilities & Cleaning': [
        ('Hospital Grade Disinfectant', 45.00), 
        ('Paper Towels (Case)', 32.00), 
        ('Biohazard Bags', 15.00)
    ],
    'IT & Admin': [
        ('Office Paper (Case)', 35.00), 
        ('Printer Toner', 85.00), 
        ('Staff Laptops', 850.00)
    ]
}

suppliers = ['MediSupply Co.', 'HealthFlow Logistics', 'Global Hygiene', 'TechMed Solutions']

# --- GENERATE DATA ---
data = []

for i in range(rows):
    # 1. Random Date (Last 12 months)
    date = datetime.today() - timedelta(days=random.randint(0, 365))
    
    # 2. Pick a Category and Item
    category = random.choice(list(items.keys()))
    item_name, base_price = random.choice(items[category])
    
    # 3. Simulate Price Fluctuation (The "Inflation" Factor)
    # Prices vary by -5% to +15% randomly
    price_change_pct = random.uniform(-0.05, 0.15) 
    actual_price = base_price * (1 + price_change_pct)
    
    # 4. Volume (Quantity)
    qty = random.randint(10, 500)
    
    data.append({
        'Date': date,
        'Category': category,
        'Item_Name': item_name,
        'Supplier': random.choice(suppliers),
        'Baseline_Price': round(base_price, 2),   # Contract Price
        'Actual_Price': round(actual_price, 2),   # What we paid
        'Quantity': qty,
        'Total_Spend': round(actual_price * qty, 2),
        # This is the Key Metric: How much extra did we pay?
        'Price_Variance_Impact': round((actual_price - base_price) * qty, 2)
    })

# --- SAVE FILE ---
df = pd.DataFrame(data)
df.to_excel("healthcare_data.xlsx", index=False)
print(f"✅ Generated 'healthcare_data.xlsx' with {rows} rows including Price Variance.")