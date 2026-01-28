

import os
import psycopg


# Load database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")


def migrate_schema(file_path):

    with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
    cur.execute("""
        -- ============================
        -- CREATE TABLES
        -- ============================

        -- Categories (just primary key)
        CREATE TABLE IF NOT EXISTS categories (
            category_id SERIAL PRIMARY KEY
        );

        -- Products (primary key + foreign key)
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            category_id INT REFERENCES categories(category_id)
        );

        -- Customers (primary key)
        CREATE TABLE IF NOT EXISTS customers (
            customer_id SERIAL PRIMARY KEY
        );

        -- Orders (primary key + foreign key)
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES customers(customer_id)
        );

        -- Order Items (primary key + foreign keys)
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id SERIAL PRIMARY KEY,
            order_id INT REFERENCES orders(order_id),
            product_id INT REFERENCES products(product_id)
        );

        -- ============================
        -- Add remaining columns
        -- ============================

        -- Categories
        ALTER TABLE categories ADD COLUMN IF NOT EXISTS name VARCHAR NOT NULL;

        -- Products
        ALTER TABLE products ADD COLUMN IF NOT EXISTS name VARCHAR NOT NULL;
        ALTER TABLE products ADD COLUMN IF NOT EXISTS price NUMERIC NOT NULL;
        ALTER TABLE products ADD COLUMN IF NOT EXISTS stock INT NOT NULL;

        -- Customers
        ALTER TABLE customers ADD COLUMN IF NOT EXISTS first_name VARCHAR NOT NULL;
        ALTER TABLE customers ADD COLUMN IF NOT EXISTS last_name VARCHAR NOT NULL;
        ALTER TABLE customers ADD COLUMN IF NOT EXISTS email VARCHAR UNIQUE NOT NULL;

        -- Orders
        ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_date DATE DEFAULT CURRENT_DATE;

        -- Order Items
        ALTER TABLE order_items ADD COLUMN IF NOT EXISTS quantity INT NOT NULL;
    """)
    

    def seed_sample_data(file_path):

        with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO categories (name) VALUES
            ('T-Shirts'),
            ('Jeans'),
            ('Shoes'),
            ('Accessories')
            ON CONFLICT DO NOTHING;

            INSERT INTO products (name, category_id, price, stock) VALUES
            ('Basic White T-Shirt', 1, 19.99, 100),
            ('Black Hoodie', 1, 39.99, 40),
            ('Graphic Tee', 1, 24.99, 60),
            ('Striped Polo Shirt', 1, 29.99, 50),
            ('Blue Denim Jeans', 2, 49.99, 50),
            ('Black Slim Jeans', 2, 59.99, 35),
            ('Grey Chinos', 2, 44.99, 45),
            ('Running Sneakers', 3, 89.99, 30),
            ('Leather Shoes', 3, 120.00, 20),
            ('Canvas Sneakers', 3, 69.99, 25),
            ('Leather Belt', 4, 29.99, 75),
            ('Wool Scarf', 4, 34.99, 40),
            ('Beanie Hat', 4, 19.99, 60),
            ('Sunglasses', 4, 49.99, 30)
            ON CONFLICT DO NOTHING;

            INSERT INTO customers (first_name, last_name, email) VALUES
            ('Alice', 'Johnson', 'alice@example.com'),
            ('Bob', 'Smith', 'bob@example.com'),
            ('Carol', 'Davis', 'carol@example.com')
            ON CONFLICT DO NOTHING;

            INSERT INTO orders (customer_id, order_date) VALUES
            (1, '2026-01-15'),
            (2, '2026-01-20')
            ON CONFLICT DO NOTHING;

            INSERT INTO order_items (order_id, product_id, quantity) VALUES
            (1, 1, 2),  -- Alice buys 2 Basic White T-Shirts
            (1, 4, 1),  -- Alice buys 1 Leather Belt
            (2, 2, 1),  -- Bob buys 1 Blue Denim Jeans
            (2, 3, 2)  -- Bob buys 2 Running Sneakers
            ON CONFLICT DO NOTHING;

        """)