import sqlite3
import math

PER_PAGE = 25  # 페이지당 항목 수 (필요할 때마다 여기만 수정!)


def init_db():
    conn = sqlite3.connect('cwe.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS cwe_results')
    c.execute('DROP TABLE IF EXISTS cwe_excluded')  # ❗예외처리 테이블도 초기화

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

    c.execute('''
        CREATE TABLE IF NOT EXISTS cwe_excluded (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            title TEXT,
            link TEXT UNIQUE,
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
    for title, link, *_ in results:
        try:
            c.execute(
                "INSERT INTO cwe_results (keyword, title, link) VALUES (?, ?, ?)",
                (keyword, title, link)
            )
            new_count += 1
        except sqlite3.IntegrityError:
            duplicate_count += 1
    conn.commit()
    conn.close()
    return new_count, duplicate_count

def delete_from_db(link):
    conn = sqlite3.connect('cwe.db')
    c = conn.cursor()

    # 1. 삭제 전 데이터 조회
    c.execute("SELECT keyword, title FROM cwe_results WHERE link = ?", (link,))
    row = c.fetchone()
    keyword = row[0] if row else "N/A"
    title = row[1] if row else "N/A"

    # 2. 삭제
    c.execute("DELETE FROM cwe_results WHERE link = ?", (link,))

    # 3. 예외 목록에 등록
    c.execute('''
        INSERT OR IGNORE INTO cwe_excluded (keyword, title, link)
        VALUES (?, ?, ?)
    ''', (keyword, title, link))

    conn.commit()
    conn.close()


def fetch_excluded_links():
    conn = sqlite3.connect('cwe.db')
    c = conn.cursor()
    c.execute("SELECT link FROM cwe_excluded")
    excluded = {row[0] for row in c.fetchall()}
    conn.close()
    return excluded

def fetch_from_db(page, per_page=PER_PAGE):
    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()
    offset = (page - 1) * per_page
    c.execute("SELECT COUNT(*) FROM cwe_results")
    total = c.fetchone()[0]
    total_pages = math.ceil(total / per_page)
    c.execute("SELECT keyword, title, link FROM cwe_results ORDER BY created_at DESC LIMIT ? OFFSET ?", (per_page, offset))
    results = c.fetchall()
    conn.close()
    return results, total_pages, total

def fetch_excluded(page, per_page=PER_PAGE):
    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()
    offset = (page - 1) * per_page
    c.execute("SELECT COUNT(*) FROM cwe_excluded")
    total = c.fetchone()[0]
    total_pages = math.ceil(total / per_page)

    c.execute("SELECT link FROM cwe_excluded ORDER BY id DESC LIMIT ? OFFSET ?", (per_page, offset))
    results = c.fetchall()
    conn.close()
    return results, total_pages, total

def fetch_excluded_from_db(page, per_page=PER_PAGE):
    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()
    offset = (page - 1) * per_page
    c.execute("SELECT COUNT(*) FROM cwe_excluded")
    total = c.fetchone()[0]
    total_pages = math.ceil(total / per_page)

    c.execute("SELECT keyword, title, link FROM cwe_excluded ORDER BY id DESC LIMIT ? OFFSET ?", (per_page, offset))
    results = c.fetchall()
    conn.close()
    return results, total_pages, total

