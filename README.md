# 🔍 CWE 키워드 기반 자동 크롤링 시스템

VisualPro에서 반복적으로 수동 확인하던 보안 정보를 자동으로 수집하는 프로젝트입니다.  
MITRE의 [CWE 공식 웹사이트](https://cwe.mitre.org/)를 기반으로 키워드를 입력하면 관련된 CWE 항목을 크롤링하고, 결과를 DB에 저장하여 웹 UI로 관리할 수 있습니다.

---

## 🚀 주요 기능

- ✅ 키워드 기반 CWE 검색
- ✅ Playwright로 다중 페이지 자동 크롤링
- ✅ 검색 결과 DB 저장 (SQLite)
- ✅ 중복 필터링
- ✅ 웹 기반 입력 폼 + 결과 뷰
- ✅ 페이지네이션 지원
- ✅ DB 초기화 기능

---

## 🧰 사용 기술

- Python 3.x
- Flask (백엔드)
- Playwright (브라우저 자동화)
- SQLite (로컬 DB)

---

## 📦 설치 방법
git clone https://github.com/dhchoi95/vulner.git
cd vulner
**.
pip install flask playwright
python -m playwright install
.**

🖥️ 실행 방법
설치 폴더 경로에서
python app.py
브라우저에서 http://localhost:5000 접속

키워드 입력 → 결과 크롤링 → 저장된 CWE 확인 가능

🗃️ DB 초기화
curl -X POST http://localhost:5000/reset_db
또는 페이지 하단의 DB 초기화 버튼을 클릭하세요.

📁 향후 확장 가능성
 NVD CVE 검색 연동
 Slack / Email 알림
 검색 예약 스케줄러
 VP 시스템 자동 업로드 연결

