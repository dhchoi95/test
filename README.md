# ✅ requirements.txt (Render가 설치할 패키지 목록)
Flask
playwright
beautifulsoup4
openai
python-dotenv

# playwright 설치 후 실행에 필요한 브라우저 설치 명령은 Render에서 실행 불가이므로 local에서 playwright install 해두는 게 좋습니다


# ✅ .gitignore (GitHub에 올리지 말아야 할 파일)
__pycache__/
.env
cwe.db
*.pyc
*.log


# ✅ README.md (Render 배포용 가이드)

# CWE Keyword Scraper Web App

A simple Flask-based app to search for CWE entries and store results, designed for deployment on Render.

## 📦 Features
- Keyword search with default or manual input
- SQLite database for result storage
- Pagination UI

## 🚀 Deploying on Render

### 1. Prepare Repository
Upload these files to your GitHub repository:
- app.py
- model.py
- scraper.py
- templates/result.html
- requirements.txt
- .gitignore

### 2. Create Web Service on Render
- Go to [https://render.com](https://render.com) and create a new Web Service
- Choose your GitHub repository
- Use these settings:
  - **Build Command:** pip install -r requirements.txt
  - **Start Command:** python app.py
  - **Environment:** Python
  - **Free Plan:** Yes

### 3. (Optional) Set Environment Variable
If using GPT:
OPENAI_API_KEY=sk-xxxxxxx


Go to **Render → Your Service → Environment → Add Environment Variable**

### 4. Run
Once deployed, visit your live site at:
https://your-app-name.onrender.com


Happy scraping! 🕵️‍♀️
이 코드 어디에 어떻게 만드는 거야? 나 아무것도 안 했어