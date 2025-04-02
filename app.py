from flask import Flask, render_template, request, redirect, url_for, jsonify
from model import init_db, save_to_db, fetch_from_db
from scraper import search_cwe
import sqlite3
import math

app = Flask(__name__)

# 기본 키워드
default_keywords = [
    "ISP", "Image Signal Processor", "CIS", "CMOS", "SoC", "ROM", "RAM", "ECU", "Thermistor", "MCU",
    "OSC", "Oscillator", "Flash memory", "AHD", "Analog High Definition", "MIPI", "LIN", "I2C",
    "SPI", "QSPI", "GPIO", "JTAG", "UART", "NEXTCHIP", "PARTS", "GAONCHIPS", "SAMSUNG", "ARM",
    "JTAG Debugger", "Clock signal", "Reset signal", "Peripherals", "Power"
]

@app.route("/", methods=["GET"])
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        results = search_cwe(keyword)
        save_to_db(keyword, results)

    page = int(request.args.get("page", 1))
    db_results, total_pages = fetch_from_db(page)
    return render_template("result.html", results=db_results, page=page, total_pages=total_pages)

@app.route("/search_default", methods=["POST"])
def search_default():
    for kw in default_keywords:
        try:
            print(f"🔍 {kw} 검색 중...")
            results = search_cwe(kw)
            new_count, duplicate_count = save_to_db(kw, results)
            print(f"✅ 저장 완료: {kw} - 신규 {new_count} / 중복 {duplicate_count}")
        except Exception as e:
            print(f"❌ 오류: {kw} - {e}")
    return redirect(url_for("search"))

@app.route("/search_keyword", methods=["POST"])
def search_keyword():
    keyword = request.form.get("keyword")
    try:
        results = search_cwe(keyword)
        new_items = save_to_db(keyword, results)[0]
        html_fragments = "".join([
            f"<li><strong>{keyword}</strong>: <a href='{link}' target='_blank'>{title}</a></li>"
            for (title, link, desc, mit) in results
        ])
        return jsonify({"new_count": new_items, "html": html_fragments})
    except Exception as e:
        return jsonify({"new_count": 0, "html": f"<li><strong>{keyword}</strong>: 오류 - {str(e)}</li>"}), 500

@app.route("/reset_db", methods=["POST"])
def reset_db():
    init_db()
    return redirect(url_for("search"))

if __name__ == "__main__":
    # init_db()  # 초기화 원할 경우만 사용
    app.run(debug=True)
