from playwright.sync_api import sync_playwright


def search_cwe(keyword, max_pages=10):
    result_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(15000)
        page.goto("https://cwe.mitre.org/")
        page.fill('input[name="search"]', keyword)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

        # captcha 감지 시도
        if page.locator('iframe[src*="recaptcha"]').count() > 0:
            print("⚠️ 로봇 검증 화면이 떴어요! 브라우저에서 수동으로 인증해 주세요.")
            input("✅ 인증 완료 후 Enter 키를 눌러 계속 진행합니다...")

        page_num = 1
        while page_num <= max_pages:
            results = page.locator('a.gs-title')
            count = results.count()
            for i in range(count):
                title = results.nth(i).inner_text()
                if "CWE-" in title:
                    href = results.nth(i).get_attribute("href")

                    desc, mit = "N/A", "N/A"
                    print(f"✅ {title}\n📘 Desc: {desc}\n🛡️ Mit: {mit}\n")

                    result_list.append((title, href, desc, mit))

            next_button = page.locator(f'div.gsc-cursor-page:has-text("{page_num + 1}")')
            if next_button.count() > 0:
                next_button.first.click()
                page.wait_for_timeout(1000)
                page_num += 1
            else:
                break

        browser.close()
    return result_list
