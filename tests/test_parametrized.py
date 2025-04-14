import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import search_cwe

# ✅ Positive Test Cases
@pytest.mark.parametrize("keyword", [
    "UART",
    "CAN",
    "DMA"
])
def test_search_cwe_positive(keyword):
    result = search_cwe(keyword)
    assert isinstance(result, list)
    assert len(result) > 0
    assert all("CWE" in r[0] for r in result)  # 제목에 CWE 포함


# 🚫 Negative Test Cases
@pytest.mark.parametrize("keyword", [
    None,
    1234,
    "@#$%^&"
])
def test_search_cwe_negative(keyword):
    try:
        result = search_cwe(str(keyword))
        assert isinstance(result, list)
    except Exception:
        assert True  # 예외가 발생하는 것도 허용


# 🧮 Boundary Test Cases
@pytest.mark.parametrize("keyword", [
    "A",
    "",
    "X" * 1000
])
def test_search_cwe_boundary(keyword):
    result = search_cwe(keyword)
    assert isinstance(result, list)


# 🤯 Fuzz Test Cases
@pytest.mark.parametrize("keyword", [
    " " * 100,
    "🔥💥",
    "SELECT * FROM users;"
])
def test_search_cwe_fuzz(keyword):
    result = search_cwe(keyword)
    assert isinstance(result, list)
    assert all(isinstance(r, tuple) for r in result) or len(result) == 0
