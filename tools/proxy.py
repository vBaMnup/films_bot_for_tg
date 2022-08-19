import requests
from bs4 import BeautifulSoup as bs

from config import PROXY_URL
from user_agent import get_random_user_agent


def get_proxies():
    parsed_proxies_list = bs(requests.get(
        PROXY_URL,
        headers=get_random_user_agent()
    ).content, 'html.parser'
    )
    proxies = []
