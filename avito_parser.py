import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumbase import SB


def get_links():
    options = Options()
    options.add_argument('--headless')
    with SB(uc=True,
       headless=True,
       page_load_strategy="eager",
       block_images=True,
       # skip_js_waits=True,
       ) as driver:
        base_url_phone = 'https://www.avito.ru/krasnoyarsk/telefony/mobilnye_telefony/apple/iphone-ASgBAgICA0SywA202Di0wA3OqzmwwQ2I_Dc?cd=1&s=104'
        driver.open(base_url_phone)

        if "Доступ ограничен" in driver.get_title():
            time.sleep(10)
            raise Exception("Перезапуск из-за блокировки IP")
        ads = []
        driver.open_new_window()  # сразу открываем и вторую вкладку
        driver.switch_to_window(window=0)

        item_elements = driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        for item in item_elements:
            try:
                if item.find_element(By.CSS_SELECTOR, '[class=SnippetBadge-title-oSImJ]'):
                    url = item.find_element(By.CSS_SELECTOR, '[itemprop=url]').get_attribute("href")
                    ads.append(url)
            except:
                pass
        return ads
print(get_links())