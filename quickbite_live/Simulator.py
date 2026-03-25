import pyodbc
import csv
import os
import time
import random
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────
SERVER   = "DESKTOP-DCENTG8"  # your PC name — change if needed
DATABASE = "quickbite"
CSV_PATH = r"C:\Users\ELYON\Data Analysis\Python\venv\quickbite_live\data\orders.csv"

CONN_STR = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)

BRANCHES = ["Independence Layout", "Ogui Road", "GRA", "New Haven", "Trans-Ekulu"]
CASHIERS = ["Adaeze", "Emeka", "Chioma", "Uche", "Ngozi", "Chukwudi"]
PAYMENTS = ["Cash", "POS", "Transfer"]

MENU = {
    "Jollof Rice":      850,
    "Fried Rice":       900,
    "Shawarma":         1200,
    "Chicken Burger":   1500,
    "Peppered Chicken": 1100,
    "Chips & Chicken":  1300,
    "Moi Moi":          500,
    "Zobo Drink":       300,
    "Chapman":          600,
    "Meat Pie":         400,
}

# ── SETUP ───────────────────────────────────────────────
def setup():
    os.makedirs("data", exist_ok=True)

    # CSV header
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "order_id", "timestamp", "branch", "cashier",
                "item", "quantity", "unit_price", "total_price", "payment"
            ])

# ── GENERATE ONE ORDER ───────────────────────────────────
def generate_order():
    item       = random.choice(list(MENU.keys()))
    quantity   = random.randint(1, 5)
    unit_price = MENU[item]
    total      = unit_price * quantity

    return {
        "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "branch":      random.choice(BRANCHES),
        "cashier":     random.choice(CASHIERS),
        "item":        item,
        "quantity":    quantity,
        "unit_price":  unit_price,
        "total_price": total,
        "payment":     random.choice(PAYMENTS),
    }

# ── SAVE ORDER ───────────────────────────────────────────
def save_order(order):
    # Save to SQL Server
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (timestamp, branch, cashier, item, quantity, unit_price, total_price, payment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, order["timestamp"], order["branch"], order["cashier"],
         order["item"], order["quantity"], order["unit_price"],
         order["total_price"], order["payment"])
    
    cursor.execute("SELECT @@IDENTITY")
    order_id = int(cursor.fetchone()[0])
    conn.commit()
    conn.close()

    # Save to CSV
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            order_id, order["timestamp"], order["branch"], order["cashier"],
            order["item"], order["quantity"], order["unit_price"],
            order["total_price"], order["payment"]
        ])

    return order_id

# ── MAIN LOOP ────────────────────────────────────────────
if __name__ == "__main__":
    setup()
    print("✅ QuickBite Simulator started — new order every 15 seconds\n")

    while True:
        order    = generate_order()
        order_id = save_order(order)
        print(f"[{order['timestamp']}] Order #{order_id} | {order['branch']} | "
              f"{order['item']} x{order['quantity']} | ₦{order['total_price']:,} | {order['payment']}")
        time.sleep(15)