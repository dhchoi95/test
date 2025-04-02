import sqlite3
import math

def init_db():
    conn = sqlite3.connect('cwe.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS cwe_results')
    c.execute('''
        CREATE TABLE IF NOT EXISTS cwe_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            title TEXT,
            link TEXT UNIQUE,
            description TEXT,
            mitigation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(keyword, results):
    conn = sqlite3.connect('cwe.db')
    c = conn.cursor()
    new_count = 0
    duplicate_count = 0

    for title, link, desc, mit in results:
        try:
            c.execute('''
                INSERT INTO cwe_results (keyword, title, link, description, mitigation)
                VALUES (?, ?, ?, ?, ?)
            ''', (keyword, title, link, desc, mit))
            new_count += 1
        except sqlite3.IntegrityError:
            duplicate_count += 1

    conn.commit()
    conn.close()
    return new_count, duplicate_count

def fetch_from_db(page, per_page=30):
    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()
    offset = (page - 1) * per_page
    c.execute("SELECT COUNT(*) FROM cwe_results")
    total = c.fetchone()[0]
    total_pages = math.ceil(total / per_page)

    c.execute("SELECT keyword, title, link, description, mitigation FROM cwe_results ORDER BY created_at DESC LIMIT ? OFFSET ?", (per_page, offset))
    results = c.fetchall()
    conn.close()
    return results, total_pages
