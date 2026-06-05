import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_name="shop.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT,
                barcode TEXT UNIQUE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_code TEXT UNIQUE NOT NULL,
                customer_name TEXT,
                items TEXT,
                total REAL,
                status TEXT DEFAULT 'pending',
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_code TEXT,
                event TEXT,
                timestamp TEXT,
                location TEXT
            )
        ''')
        self.conn.commit()
    
    def add_product(self, name, price, category, barcode):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, category, barcode) VALUES (?,?,?,?)",
            (name, price, category, barcode)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_product_by_barcode(self, barcode):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE barcode=?", (barcode,))
        return cursor.fetchone()
