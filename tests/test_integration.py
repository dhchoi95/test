# tests/test_integration.py
import pytest
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# 실제 크롤링을 수행하므로 시간 소요 있음
# 결과를 선택 및 저장하는 단계는 수동 시뮬레이션 필요

def test_full_search_to_save_flow(client):
    # Step 1: 검색 요청
    response = client.post("/search", data={"keyword": "UART"})
    assert response.status_code == 200

    response_text = response.data.decode("utf-8")
    assert "CWE" in response_text or "검색 결과" in response_text

    # Step 2: 결과 저장 시뮬레이션
    title = "CWE-999: 테스트 저장 항목"
    link = "https://example.com/test-integration"
    keyword = "UART"
    selected = f"{title}|||{link}|||{keyword}"
    save_response = client.post("/add_selected", data={"selected": [selected]})
    assert save_response.status_code == 302

    # Step 3: DB 확인
    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()
    c.execute("SELECT title, link FROM cwe_results WHERE link = ?", (link,))
    row = c.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == title
