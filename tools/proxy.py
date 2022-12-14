import logging

import requests
from bs4 import BeautifulSoup

from config import PROXY_URL

from .user_agent import get_random_user_agent


def get_proxies():
    logging.info('Пробую получить список прокси с сайта')
    parsed_proxies_list = BeautifulSoup(requests.get(
        PROXY_URL,
        headers=get_random_user_agent()
    ).content, 'html.parser'
    )
    proxies = []
    for row in parsed_proxies_list.find("div",
                                        attrs={"class": "table_block"}
                                        ).find("tbody").find_all("tr")[1:]:
        tds = row.find_all('td')
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            country = tds[2].text.strip()
            type_pr = tds[4].text.strip()
            if type_pr == 'SOCKS4, SOCKS5':
                continue
            if country.startswith('Russian'):
                continue
            host = f'{type_pr}://{ip}:{port}'
            proxies.append(host)
        except IndexError as error:
            logging.error(error)
    logging.info('Список прокси получен')
    return proxies


if __name__ == '__main__':
    print(get_random_user_agent())
    print(get_proxies())
