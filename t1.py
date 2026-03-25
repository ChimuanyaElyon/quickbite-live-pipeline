import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define parameters
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 30)
date_range = pd.date_range(start=start_date, end=end_date, freq='h')  # FIXED: lowercase 'h'

# Locations
locations = ['Brooklyn Heights', 'Upper East Side', 'Greenwich Village', 'Williamsburg']

# Product categories and items with prices
products = {
    'Coffee': {
        'Americano': {'S': 2.50, 'M': 3.00, 'L': 3.50},
        'Cappuccino': {'S': 3.25, 'M': 3.75, 'L': 4.25},
        'Latte': {'S': 3.50, 'M': 4.00, 'L': 4.50},
        'Flat White': {'S': 3.75, 'M': 4.25, 'L': 4.75},
        'Cold Brew': {'S': 3.00, 'M': 3.50, 'L': 4.00},
    },
    'Tea': {
        'Green Tea': {'S': 2.25, 'M': 2.75, 'L': 3.25},
        'English Breakfast': {'S': 2.25, 'M': 2.75, 'L': 3.25},
        'Chamomile': {'S': 2.50, 'M': 3.00, 'L': 3.50},
        'Matcha Latte': {'S': 4.00, 'M': 4.50, 'L': 5.00},
    },
    'Bakery': {
        'Croissant': {'Regular': 3.50},
        'Blueberry Muffin': {'Regular': 3.25},
        'Chocolate Chip Cookie': {'Regular': 2.50},
        'Banana Bread': {'Regular': 3.00},
        'Bagel': {'Regular': 2.75},
    },
    'Specialty': {
        'Smoothie Bowl': {'Regular': 7.50},
        'Avocado Toast': {'Regular': 8.00},
        'Breakfast Sandwich': {'Regular': 6.50},
    },
    'Beans': {
        'House Blend Beans': {'250g': 12.00, '500g': 22.00},
        'Single Origin Beans': {'250g': 15.00, '500g': 28.00},
    }
}

# Generate transactions
transactions = []
transaction_id = 1

for timestamp in date_range:
    hour = timestamp.hour
    day_of_week = timestamp.weekday()
    month = timestamp.month
    
    # Determine number of transactions based on hour and day
    base_transactions = 0
    
    # Store opening hours: 6 AM - 10 PM
    if 6 <= hour < 10:  # Morning rush
        base_transactions = random.randint(8, 15)
    elif 10 <= hour < 12:  # Late morning
        base_transactions = random.randint(4, 8)
    elif 12 <= hour < 14:  # Lunch rush
        base_transactions = random.randint(6, 12)
    elif 14 <= hour < 17:  # Afternoon
        base_transactions = random.randint(3, 7)
    elif 17 <= hour < 19:  # Evening
        base_transactions = random.randint(5, 10)
    elif 19 <= hour < 22:  # Late evening
        base_transactions = random.randint(2, 5)
    
    # Weekend adjustment (slightly lower on Sunday, higher on Saturday)
    if day_of_week == 5:  # Saturday
        base_transactions = int(base_transactions * 1.15)
    elif day_of_week == 6:  # Sunday
        base_transactions = int(base_transactions * 0.85)
    
    # Seasonal adjustment (increase in spring/summer)
    if month in [5, 6]:  # May, June
        base_transactions = int(base_transactions * 1.25)
    elif month in [3, 4]:  # March, April
        base_transactions = int(base_transactions * 1.10)
    
    # Generate transactions for this hour
    for _ in range(base_transactions):
        location = random.choice(locations)
        category = random.choices(
            list(products.keys()),
            weights=[50, 20, 15, 10, 5],  # Coffee is most popular
            k=1
        )[0]
        
        product_name = random.choice(list(products[category].keys()))
        size = random.choice(list(products[category][product_name].keys()))
        price = products[category][product_name][size]
        
        # Add some random variation to exact timestamp
        exact_time = timestamp + timedelta(minutes=random.randint(0, 59))
        
        transactions.append({
            'transaction_id': transaction_id,
            'timestamp': exact_time,
            'date': exact_time.date(),
            'time': exact_time.time(),
            'day_of_week': exact_time.strftime('%A'),
            'month': exact_time.strftime('%B'),
            'location': location,
            'category': category,
            'product_name': product_name,
            'size': size,
            'unit_price': price,
            'quantity': 1  # Assuming 1 item per line
        })
        
        transaction_id += 1

# Create DataFrame
df = pd.DataFrame(transactions)

# Calculate total price
df['total_price'] = df['unit_price'] * df['quantity']

# Sort by timestamp
df = df.sort_values('timestamp').reset_index(drop=True)

# Display summary statistics
print("=" * 60)
print("COFFEE SHOP SALES DATASET - SUMMARY")
print("=" * 60)
print(f"\nTotal Transactions: {len(df):,}")
print(f"Total Revenue: ${df['total_price'].sum():,.2f}")
print(f"Average Transaction Value: ${df['total_price'].mean():.2f}")
print(f"Date Range: {df['date'].min()} to {df['date'].max()}")
print(f"\nTransactions by Location:")
print(df['location'].value_counts().to_string())
print(f"\nTransactions by Category:")
print(df['category'].value_counts().to_string())
print(f"\nTop 10 Products by Revenue:")
print(df.groupby('product_name')['total_price'].sum().sort_values(ascending=False).head(10).to_string())

print("\n" + "=" * 60)
print("First 10 rows of the dataset:")
print("=" * 60)
print(df.head(10).to_string())

# Save to CSV
csv_filename = 'coffee_shop_sales_data.csv'
df.to_csv(csv_filename, index=False)
print(f"\n✓ Dataset saved as '{csv_filename}'")
print(f"✓ Total rows: {len(df):,}")
print("\nYou can now download this file and practice your analysis!")
