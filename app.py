from flask import Flask, render_template, request, redirect, url_for
from model import init_db, save_to_db, delete_from_db, fetch_excluded_from_db
from scraper import search_cwe
import sqlite3
import math

app = Flask(__name__)
PER_PAGE = 25  # 페이지당 항목 수 (필요할 때마다 여기만 수정!)

default_keywords = [
    "ISP", "Image Signal Processor", "CIS", "CMOS", "SoC", "ROM", "RAM", "ECU", "Thermistor", "MCU",
    "OSC", "Oscillator", "Flash memory", "AHD", "Analog High Definition", "MIPI", "LIN", "I2C",
    "SPI", "QSPI", "GPIO", "JTAG", "UART", "NEXTCHIP", "PARTS", "GAONCHIPS", "SAMSUNG", "ARM",
    "JTAG Debugger", "Clock signal", "Reset signal", "Peripherals", "Power"
]

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

@app.route("/", methods=["GET"])
@app.route("/search", methods=["GET", "POST"])
def search():
    new_results = []

    if request.method == "POST":
        keyword = request.form.get("keyword")
        all_results = search_cwe(keyword)
        all_results = [(title, link, keyword) for (title, link, *_) in all_results]

        conn = sqlite3.connect("cwe.db")
        c = conn.cursor()
        c.execute("SELECT link FROM cwe_results")
        existing_links = {row[0] for row in c.fetchall()}
        c.execute("SELECT link FROM cwe_excluded")
        excluded_links = {row[0] for row in c.fetchall()}
        conn.close()

        new_results = [item for item in all_results if item[1] not in existing_links | excluded_links]

    page = int(request.args.get("page", 1))
    excluded_page_raw = request.args.get("excluded_page", "1")
    excluded_page = int(excluded_page_raw) if excluded_page_raw.isdigit() else 1
    db_results, total_pages, total_items = fetch_from_db(page)
    excluded_results, excluded_total_pages, excluded_total_items = fetch_excluded_from_db(excluded_page)

    enumerated_results = [
        (total_items - ((page - 1) * PER_PAGE + idx), keyword, title, link)
        for idx, (keyword, title, link) in enumerate(db_results)
    ]

    enumerated_excluded = [
        (excluded_total_items - ((page - 1) * PER_PAGE + idx), keyword, title, link)
        for idx, (keyword, title, link) in enumerate(excluded_results)
    ]

    return render_template("result.html",
        results=enumerated_results,
        page=page,
        total_pages=total_pages,
        new_results=new_results,
        default_keywords=default_keywords,
        excluded=enumerated_excluded,
        excluded_total_pages=excluded_total_pages,
        excluded_page=excluded_page  # ✅ 이 줄 추가
    )

@app.route("/add_selected", methods=["POST"])
def add_selected():
    selected_items = request.form.getlist("selected")

    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()
    for item in selected_items:
        try:
            title, link, keyword = item.split("|||")
            c.execute("INSERT INTO cwe_results (keyword, title, link) VALUES (?, ?, ?)", (keyword, title, link))
        except sqlite3.IntegrityError:
            continue
    conn.commit()
    conn.close()

    return redirect(url_for("search"))

@app.route("/search_selected", methods=["POST"])
def search_selected():
    selected_keywords = request.form.getlist("keywords")
    mode = request.form.get("mode")
    new_results = []

    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()
    c.execute("SELECT link FROM cwe_results")
    existing_links = {row[0] for row in c.fetchall()}
    c.execute("SELECT link FROM cwe_excluded")
    excluded_links = {row[0] for row in c.fetchall()}
    conn.close()

    for kw in selected_keywords:
        try:
            results = search_cwe(kw)
            results_with_kw = [(title, link, kw) for (title, link, *_) in results]
            fresh_results = [r for r in results_with_kw if r[1] not in existing_links | excluded_links]
            if mode == "save":
                save_to_db(kw, fresh_results)
            else:
                new_results.extend(fresh_results)
        except Exception as e:
            print(f"❌ 오류: {kw} - {e}")

    if mode == "save":
        return redirect(url_for("search"))
    else:
        page = 1
        excluded_page = 1
        db_results, total_pages, total_items = fetch_from_db(page)
        excluded_results, excluded_total_pages, excluded_total_items = fetch_excluded_from_db(excluded_page)

        enumerated_results = [
            (total_items - ((page - 1) * PER_PAGE + idx), keyword, title, link)
            for idx, (keyword, title, link) in enumerate(db_results)
        ]
        enumerated_excluded = [
            (excluded_total_items - ((excluded_page - 1) * PER_PAGE + idx), keyword, title, link)
            for idx, (keyword, title, link) in enumerate(excluded_results)
        ]

        return render_template("result.html",
            results=enumerated_results,
            page=page,
            total_pages=total_pages,
            new_results=new_results,
            default_keywords=default_keywords,
            excluded=enumerated_excluded,
            excluded_total_pages=excluded_total_pages,
            excluded_page=excluded_page  # ✅ 이 줄 추가
        )

@app.route("/reset_db", methods=["POST"])
def reset_db():
    init_db()
    return redirect(url_for("search"))

@app.route("/delete", methods=["POST"])
def delete():
    link = request.form.get("link")
    delete_from_db(link)
    return redirect(request.referrer or url_for("search"))

@app.route("/delete_excluded", methods=["POST"])
def delete_excluded():
    link = request.form.get("link")
    conn = sqlite3.connect("cwe.db")
    c = conn.cursor()
    c.execute("DELETE FROM cwe_excluded WHERE link = ?", (link,))
    conn.commit()
    conn.close()
    return redirect(request.referrer or url_for("search"))

if __name__ == "__main__":
    app.run(debug=True)
