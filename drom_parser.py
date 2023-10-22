import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def get_links():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    print('Start drom')
    base_url_phone = 'https://krasnoyarsk.drom.ru/auto/'
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    request = requests.get(base_url_phone, headers=hdr)
    soup = BeautifulSoup(request.text, 'lxml')
    good_cost = soup.find_all('a')
    links = []
    for good in good_cost:
        div = good.find('div', class_='css-1p9rl0p ejipaoe0')
        if div and div.text == 'хорошая цена':
            links.append(good.get('href'))
    return links

