# tests/test_model.py
import sqlite3
from model import init_db, save_to_db, delete_from_db


def test_init_db_creates_tables():
    # DB 초기화
    init_db()

    # DB 연결 후 테이블 목록 확인
    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in c.fetchall()]
    conn.close()

    # 결과 검증
    assert "cwe_results" in tables
    assert "cwe_excluded" in tables

def test_save_to_db_inserts_data():
    # 준비: 초기화
    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()
    c.execute("DELETE FROM cwe_results")  # 기존 데이터 제거
    conn.commit()

    # 테스트 대상 실행
    test_keyword = "UART"
    test_data = [("CWE-123: UART 버퍼 오버플로우", "https://example.com/cwe-123", test_keyword)]
    save_to_db(test_keyword, test_data)

    # 검증: DB에서 방금 넣은 데이터가 있는지 확인
    c.execute("SELECT keyword, title, link FROM cwe_results WHERE keyword = ?", (test_keyword,))
    rows = c.fetchall()
    conn.close()

    assert len(rows) == 1
    assert rows[0][0] == test_keyword
    assert "UART" in rows[0][1]



def test_delete_from_db_removes_entry():
    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()

    # 테스트용 데이터 삽입
    test_keyword = "UART"
    test_title = "CWE-999: 테스트용 삭제 항목"
    test_link = "https://example.com/delete-me"
    c.execute("INSERT INTO cwe_results (keyword, title, link) VALUES (?, ?, ?)",
              (test_keyword, test_title, test_link))
    conn.commit()

    # 삭제 수행
    delete_from_db(test_link)

    # 삭제 확인
    c.execute("SELECT * FROM cwe_results WHERE link = ?", (test_link,))
    result = c.fetchall()
    conn.close()

    assert result == []
