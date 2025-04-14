import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ✅ Positive Test Cases
@pytest.mark.parametrize("keyword", ["UART", "CAN", "DMA"])
def test_search_positive(client, keyword):
    response = client.post("/search", data={"keyword": keyword})
    assert response.status_code == 200
    response_text = response.data.decode("utf-8")
    assert "검색 결과" in response_text or "CWE" in response_text


# 🚫 Negative Test Cases
@pytest.mark.parametrize("keyword", [None, 1234, "@#$%^&"])
def test_search_negative(client, keyword):
    response = client.post("/search", data={"keyword": str(keyword)})
    assert response.status_code == 200
    response_text = response.data.decode("utf-8")
    assert "검색 결과" in response_text or "CWE" in response_text or "검색어를 입력해주세요" in response_text


# 🧮 Boundary Test Cases
@pytest.mark.parametrize("keyword", ["A", "", "X" * 1000])
def test_search_boundary(client, keyword):
    response = client.post("/search", data={"keyword": keyword})
    assert response.status_code == 200
    response_text = response.data.decode("utf-8")
    assert "검색 결과" in response_text or "CWE" in response_text or "검색어를 입력해주세요" in response_text


# 🤯 Fuzz Test Cases
@pytest.mark.parametrize("keyword", ["🔥💥", " " * 100, "SELECT * FROM users;"])
def test_search_fuzz(client, keyword):
    response = client.post("/search", data={"keyword": keyword})
    assert response.status_code == 200
    response_text = response.data.decode("utf-8")
    assert "검색 결과" in response_text or "CWE" in response_text or "검색어를 입력해주세요" in response_text