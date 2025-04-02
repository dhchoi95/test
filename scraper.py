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

        # ✅ 충분히 기다려주기
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        if page.locator('iframe[src*="recaptcha"]').count() > 0:
            print("⚠️ 로봇 검증 화면이 떴어요! 브라우저에서 수동으로 인증해 주세요.")
            input("✅ 인증 후 Enter를 누르세요...")

        page_num = 1
        while page_num <= max_pages:
            results = page.locator('a.gs-title')
            count = results.count()

            for i in range(count):
                title = results.nth(i).inner_text()
                if "CWE-" in title and not title.strip().startswith("VIEW:"):
                    href = results.nth(i).get_attribute("href")
                    result_list.append((title, href, "N/A", "N/A"))

            # ✅ 다음 페이지 버튼이 보일 때까지 기다림
            next_button = page.locator(f'div.gsc-cursor-page:has-text("{page_num + 1}")')
            if next_button.count() > 0:
                next_button.first.scroll_into_view_if_needed()
                next_button.first.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2000)
                page_num += 1
            else:
                break

        browser.close()
    return result_list
