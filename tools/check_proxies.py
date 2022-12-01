import logging

from config import TIMEOUT
from tools.proxy import get_proxies
from tools.user_agent import get_random_user_agent

LIST_BAD_PROXY = set()


def check_proxy(session, url):
    """
    Ищем рабочий прокси из списка
    :return:
    """
    logging.info('Начинаю поиск рабочего прокси')
    while True:
        for proxy in get_proxies():
            if proxy in LIST_BAD_PROXY:
                continue
            random_proxy = {'http': proxy, 'https': proxy}
            try:
                request = session.get(url,
                                           headers=get_random_user_agent(),
                                           proxies=random_proxy,
                                           timeout=TIMEOUT)
                if request.status_code != 200:
                    assert Exception(f'Прокси "{random_proxy}" '
                                     f'вернул не верный статус-код')
                logging.info(f'Найден рабочий прокси: {random_proxy}')
                LIST_BAD_PROXY.add(proxy)
                return random_proxy
            except Exception:
                LIST_BAD_PROXY.add(proxy)
                logging.error(f'Прокси {random_proxy} не смог подключиться')