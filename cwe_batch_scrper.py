# cwe_batch_scraper.py

from model import save_to_db
from scraper import search_cwe

keywords = [
    "ISP", "Image Signal Processor",
    "CIS", "CMOS",
    "SoC", "ROM", "RAM", "ECU", "Thermistor", "MCU",
    "OSC", "Oscillator",
    "Flash memory",
    "AHD", "Analog High Definition",
    "MIPI", "LIN", "I2C", "SPI", "QSPI",
    "GPIO", "JTAG", "UART",
    "NEXTCHIP", "PARTS", "GAONCHIPS", "SAMSUNG", "ARM",
    "JTAG Debugger", "Clock signal", "Reset signal", "Peripherals", "Power"
]

for kw in keywords:
    try:
        print(f"🔍 {kw} 검색 중...")
        results = search_cwe(kw, max_pages=10)
        new_count, duplicate_count = save_to_db(kw, results)
        print(f"✅ 저장 완료: {kw} - 신규 {new_count}개 / 중복 {duplicate_count}개\n")
    except Exception as e:
        print(f"❌ 오류 발생: {kw} - {e}")