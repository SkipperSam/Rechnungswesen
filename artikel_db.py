import sqlite3
import os

DB_FILE = "data/artikel.db"

def init_artikel_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS artikel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            preis REAL NOT NULL,
            mwst REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_artikel(name, preis, mwst):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO artikel (name, preis, mwst) VALUES (?, ?, ?)", (name, preis, mwst))
    conn.commit()
    conn.close()

def update_artikel(artikel_id, name, preis, mwst):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE artikel SET name=?, preis=?, mwst=? WHERE id=?", (name, preis, mwst, artikel_id))
    conn.commit()
    conn.close()

def delete_artikel(artikel_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM artikel WHERE id=?", (artikel_id,))
    conn.commit()
    conn.close()

def get_alle_artikel():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, preis, mwst FROM artikel")
    artikel = c.fetchall()
    conn.close()
    return artikel

def get_artikel_by_id(artikel_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, preis, mwst FROM artikel WHERE id = ?", (artikel_id,))
    artikel = c.fetchone()
    conn.close()
    return artikel