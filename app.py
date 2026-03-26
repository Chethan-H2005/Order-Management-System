from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 🔥 Create products table and insert sample data (run once)
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER
)
""")

# Insert only if empty
cursor.execute("SELECT * FROM products")
data = cursor.fetchall()

if len(data) == 0:
    cursor.execute("INSERT INTO products (name, price) VALUES ('Phone', 10000)")
    cursor.execute("INSERT INTO products (name, price) VALUES ('Laptop', 50000)")
    cursor.execute("INSERT INTO products (name, price) VALUES ('Headphones', 2000)")

conn.commit()
conn.close()


# 🏠 Home Page (Show products in dropdown)
@app.route('/')
def home():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template('index.html', products=products)


# ➕ Add Order
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    product_id = request.form['product']   # 🔥 changed
    quantity = request.form['quantity']

    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # 🔥 orders table with product as INTEGER
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        product INTEGER,
        quantity INTEGER
    )
    """)

    cursor.execute(
        "INSERT INTO orders (name, product, quantity) VALUES (?, ?, ?)",
        (name, product_id, quantity)
    )

    conn.commit()
    conn.close()

    return redirect('/orders')


# 📊 View Orders (JOIN 🔥)
@app.route('/orders')
def orders():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT orders.id, orders.name, products.name, orders.quantity
    FROM orders
    JOIN products ON orders.product = products.id
    """)

    data = cursor.fetchall()
    conn.close()

    return render_template('orders.html', orders=data)


# ❌ Delete Order
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/orders')


if __name__ == '__main__':
    app.run(debug=True)