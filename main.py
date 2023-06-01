import requests
from bs4 import BeautifulSoup
from requests.models import ReadTimeoutError
from random import choice

def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('div', class_ = 'table-responsive').find('table').find_all('tr')[1:]
    proxies = []

    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        google = True if 'no' in tds[5].text.strip() else False
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        if schema == 'http':
            proxy = {'schema': schema, 'address': ip + ':' + port, 'google': google}
            proxies.append(proxy)
    return choice(proxies)

def get_html(url):
    p = get_proxy()
    proxy = {p['schema']: p['schema']+ '://' + p['address']}

    headers = {'Host': 'apps.sfc.hk',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://apps.sfc.hk/publicregWeb/searchByRa?locale=en',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0'}

    try:
        r = requests.get(url, timeout = 30, proxies = proxy, headers = headers)
        return r.text
    except ReadTimeoutError:
        print('Timeout error. Trying once again...')
        return get_html(url)
