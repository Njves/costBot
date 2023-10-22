import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import threading

def get_links():
    print('Start auto.ru')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    base_url_phone = 'https://auto.ru/krasnoyarsk/cars/all/?sort=cr_date-desc'
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "en-US,en-GB;q=0.9,en-RU;q=0.8,en;q=0.7,ru-RU;q=0.6,ru;q=0.5,ja-JP;q=0.4,ja;q=0.3,ar-RU;q=0.2,ar;q=0.1",
        'Cache-Control': "max-age=0",
        'Cookie': """suid=2fe7161cd21c15c2309270221bc0485e.865b58f80595559808cafdfe5d785f3f; _csrf_token=81eb20652fd66212b9f1540aa4ad025fa4b34f7f14991fa3; autoruuid=g6532a6672m4ucdnq3dt58uekpnnd31d.f7d3914b9cdb8579bf7f3f1d6b6187d1; from=google-search; autoru_sso_blocked=1; Session_id=3:1697818216.5.0.1674998948717:vQBrTg:44.1.2:1|257144043.0.2|61:10017010.607526.uU03pwp3a-gJ39KGaK8HMcjFxJM; sessar=1.1183.CiDGtLTtSxowNi_4_6DVUQXlSUAe8RTi0AT2t260oUkn3Q.mnc2A7CwSCRUC2VarDVlOEk467nzGgQWIzXaGnl4rUU; yandex_login=willhub21; ys=udn.cDp3aWxsaHViMjE%3D#c_chck.1813181508; i=9b04uKfBzkcgb1FqDBrqN5cb1TizVW8PVe6qU07/re8Mmh09NC9POvGQJhTt1RqoUg/zx9JjbX50bsjJx5THESsOlxs=; yandexuid=281002351674834971; my=YwA=; L=fmlRAgMBAEFNdVtDRVF/WwtjR1hARn9dMB9eXysAWnlY.1674998948.15237.39236.be1a49b35fb657906e1396995ad4c15d; mda2_beacon=1697818216337; sso_status=sso.passport.yandex.ru:synchronized; crookie=wPMzRhciDogMpF1W8UfTo5ThvIrmFQNZQtY6J49/XCh0HsekGJdy5etyb9EQHhvjcAYRa90VejQe9Kcawk2xylwf3ro=; cmtchd=MTY5NzgxODIyMTIzMA==; yaPassportTryAutologin=1; popups-dr-shown-count=1; autoru_sid=78807272%7C1697818229919.7776000.qJ4jYd7p_uU-V3s9ye5bDw.pYEPQub1U06l-QTZ-mzgCL60luk7MPURReWmG5NwXdk; gdpr=0; _ym_uid=1651569086980882388; _ym_isad=1; fp=56f69d07b14465d89fc3a553a3f0bb39%7C1697818230877; los=1; bltsr=1; coockoos=4; gids=62; gradius=0; _yasc=sxhobtEZt9V3XL4+kiDT8JWljSCbLVfmrlsgN/dlhOPmlKOuf1Q9mUWZWnJQ06RA0A3NMdY=; yaPlusUserPlusBalance={%22id%22:%2278807272%22%2C%22plusPoints%22:0}; count-visits=6; from_lifetime=1697819185841; _ym_d=1697819186; layout-config={"screen_height":864,"screen_width":1536,"win_width":962.4000244140625,"win_height":747.2000122070312}"""}
    request = requests.get(base_url_phone, headers=hdr)
    # <div class="OfferPriceBadgeNew-cQWc5 PriceUsedOfferNew__badge-Y9ume OfferPriceBadgeNew__gray-Fkfy3">Ниже оценки на 1%<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16" class="OfferPriceBadgeNew__arrow-AUusI"><path fill="currentColor" fill-rule="evenodd" d="m1.97 6.031 1.061-1.06 4.97 4.97 4.97-4.97 1.06 1.06-6.03 6.03-6.03-6.03Z" clip-rule="evenodd"></path></svg></div>
    soup = BeautifulSoup(request.text, 'lxml')
    good_cost = soup.find_all('a', class_='Link ListingItemTitle__link')
    links = []
    threads = []
    for good in good_cost:
        threads.append(threading.Thread(target=open, args=(good, hdr, links)))
        threads[-1].start()
    [thread.join() for thread in threads]
    return links


def open(good, hdr, links):
    page = requests.get(good.get('href'), headers=hdr)
    page.encoding = page.apparent_encoding
    child_soup = BeautifulSoup(page.text, 'lxml')
    divs = child_soup.find('div',
                           class_='OfferPriceBadgeNew-cQWc5 PriceUsedOfferNew__badge-Y9ume OfferPriceBadgeNew__gray-Fkfy3')
    if divs:
        if 'ниже оценки' in divs.text.lower():
            links.append(good.get('href'))
