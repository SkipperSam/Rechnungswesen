import sqlite3
import os

DB_FILE = "data/kunden.db"

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS kunden (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            strasse TEXT,
            plz_ort TEXT,
            geburtsdatum TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_kunde(name, strasse, plz_ort, geburtsdatum):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO kunden (name, strasse, plz_ort, geburtsdatum) VALUES (?, ?, ?, ?)", (name, strasse, plz_ort, geburtsdatum))
    conn.commit()
    conn.close()

def update_kunde(kunden_id, name, strasse, plz_ort, geburtsdatum):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE kunden SET name=?, strasse=?, plz_ort=?, geburtsdatum=? WHERE id=?", (name, strasse, plz_ort, geburtsdatum, kunden_id))
    conn.commit()
    conn.close()

def get_alle_kunden():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, strasse, plz_ort, geburtsdatum FROM kunden")
    kunden = c.fetchall()
    conn.close()
    return kunden

def get_kunde_by_id(kunden_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, strasse, plz_ort, geburtsdatum FROM kunden WHERE id = ?", (kunden_id,))
    kunde = c.fetchone()
    conn.close()
    return kunde