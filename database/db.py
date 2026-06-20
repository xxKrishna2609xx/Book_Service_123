import sqlite3
import os

# Database folder create
if not os.path.exists("database"):
    os.makedirs("database")

# Connect database
conn = sqlite3.connect("database/bookverse.db")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Purchases table
cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    book_name TEXT NOT NULL,
    payment_method TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database created successfully!")
