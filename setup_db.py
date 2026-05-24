import sqlite3

# 1. Connect to SQLite database (It will create the file automatically)
conn = sqlite3.connect('supply_chain.db')
cursor = conn.cursor()

# 2. Create the Sales Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        month TEXT,
        units_sold INTEGER
    )
''')

# 3. Insert Historical Mock Data
mock_data = [
    # Electronics
    ('Electronics', 'Jan', 100), ('Electronics', 'Feb', 120), ('Electronics', 'Mar', 115),
    ('Electronics', 'Apr', 140), ('Electronics', 'May', 130), ('Electronics', 'Jun', 160),
    # Apparel
    ('Apparel', 'Jan', 200), ('Apparel', 'Feb', 190), ('Apparel', 'Mar', 220),
    ('Apparel', 'Apr', 210), ('Apparel', 'May', 240), ('Apparel', 'Jun', 230),
    # Home Goods
    ('Home Goods', 'Jan', 50), ('Home Goods', 'Feb', 60), ('Home Goods', 'Mar', 75),
    ('Home Goods', 'Apr', 70), ('Home Goods', 'May', 90), ('Home Goods', 'Jun', 95)
]

cursor.executemany('INSERT INTO product_sales (category, month, units_sold) VALUES (?, ?, ?)', mock_data)

# Save and close
conn.commit()
conn.close()
print("🎉 Database created successfully as 'supply_chain.db'!")