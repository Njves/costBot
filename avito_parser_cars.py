import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumbase import SB


def get_links():
    print('Start avito')
    options = Options()
    options.add_argument('--headless')
    with SB(uc=True,
       headless=True,
       page_load_strategy="eager",
       block_images=True,
       # skip_js_waits=True,
       ) as driver:
        base_url_phone = 'https://www.avito.ru/krasnoyarsk/avtomobili/levyy_rul-ASgBAgICAUTwCqyKAQ?f=ASgBAgICA0TwCqyKAfIKsIoB9sQNvrA6&q=%D0%90%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B8&radius=200&s=104&searchRadius=200'
        driver.open(base_url_phone)

        if "Доступ ограничен" in driver.get_title():
            time.sleep(10)
            raise Exception("Перезапуск из-за блокировки IP")
        ads = []
        driver.open_new_window()  # сразу открываем и вторую вкладку
        driver.switch_to_window(window=0)

        item_elements = driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        print(f'Нашел {len(item_elements)}')
        for item in item_elements:
            try:
                div = item.find_element(By.CSS_SELECTOR, '[class=SnippetBadge-title-oSImJ]')
                if 'Цена ниже рыночной'.lower() == div.text.lower():
                    url = item.find_element(By.CSS_SELECTOR, '[itemprop=url]').get_attribute("href")
                    if 'krasnoyarsk' in url:
                        ads.append(url)
            except:
                pass
        return ads