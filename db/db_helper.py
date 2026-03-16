import sqlite3

DB_FILE="bank.db"

def connect():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    balance REAL NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
 )
""")
    
    conn.commit()
    conn.close()

    print("bank.db Created Successfuly🚀")