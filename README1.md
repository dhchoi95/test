# ✅ requirements.txt (Render가 설치할 패키지 목록)
Flask
playwright
beautifulsoup4
openai
python-dotenv

# ⛔ playwright 설치 후 브라우저 설치 명령 (Render에서 실행 불가하므로 local에서 먼저 실행하세요!)
# 👉 반드시 로컬에서 실행: playwright install


# ✅ .gitignore (GitHub에 올리지 말아야 할 파일들)
__pycache__/
.env
*.pyc
*.log


# ✅ README.md (Render 배포용 가이드)

# CWE Keyword Scraper Web App

A Flask-based web app to search for CWE entries, preview/save results to a database, and manage exceptions.  
Designed for deployment on [Render](https://render.com).

---

## 📦 Features

- ✅ Manual or multiple keyword-based CWE search
- ✅ Search preview before saving to DB
- ✅ Filter out duplicates and exception entries
- ✅ SQLite database to store or exclude entries
- ✅ Delete individual entries from DB or exception list
- ✅ Pagination for both DB and exception list
- ✅ 3-column layout: search area / DB list / excluded list

---

## 🚀 Deploying on Render

### 1. Prepare GitHub Repository  
Include the following files:
- app.py
- model.py
- scraper.py
- templates/result.html
- requirements.txt
- .gitignore

---

### 2. Create Web Service on Render

- Go to 👉 [https://render.com](https://render.com)
- New → **Web Service**
- Connect your GitHub repo
- Fill out settings:

| 항목 | 설정값 |
|------|--------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python app.py` |
| **Environment** | Python |
| **Free Plan** | ✔️ Yes |

---