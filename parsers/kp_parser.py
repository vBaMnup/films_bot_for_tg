import json
import logging
from urllib.parse import unquote

from requests import Session
from selectolax.parser import HTMLParser

from config import TIMEOUT
from tools.proxy import get_proxies
from tools.user_agent import get_random_user_agent

LIST_BAD_PROXY = set()


class Kparser:
    def __init__(self):
        self.session = Session()

    def check_proxy(self, url):
        """
        Ищем рабочий прокси из списка
        :return:
        """
        logging.info('Начинаю поиск рабочего прокси')
        for proxy in get_proxies():
            if proxy in LIST_BAD_PROXY:
                continue
            random_proxy = {'http': proxy, 'https': proxy}
            try:
                request = self.session.get(url,
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

    def get_json(self, url):
        """
        Получаем JSON с кинопоиска
        :param url: Ссылка на кинопоиск
        :return: Данные о фильме
        """
        while True:
            try:
                logging.info('Пытаюсь получить JSON с кинопоиска')
                proxy = self.check_proxy(url)
                request = self.session.get(url,
                                           headers=get_random_user_agent(),
                                           proxies=proxy,
                                           timeout=TIMEOUT)
                if request.status_code != 200:
                    logging.info(f'Ответ кинопоиска {request.status_code}')
                    break
                logging.info(f'Ответ кинопоиска {request.status_code}')
                tree = HTMLParser(request.text)
                scriptes = tree.css('script')

                for script in scriptes:
                    if '"@type":"Movie","url"' in script.text():
                        sc = script.text()
                        sc = unquote(sc)
                        data = json.loads(sc)
                        logging.info('Удалось получить JSON с кинопоиска')
                        return data
                logging.error('В ответе нет нужного скрипта')
            except Exception:
                logging.error('Не удалось получить JSON с кинопоиска')

    def get_content(self, data):
        logging.info('Собираю информацию о фильме')
        if 'alternateName' in data:
            name = f'{data.get("name")} / {data.get("alternateName")}'
        else:
            name = data.get("name")
        if "description" in data:
            description = data.get("description")
        else:
            description = ''
        if "aggregateRating" in data:
            ocenka = data.get("aggregateRating").get("ratingValue")
        else:
            ocenka = '-'
        if "image" in data:
            img = data.get("image").split(':')[1]
        else:
            img = 'Пусто'
        if 'genre' in data:
            ganr1 = data.get("genre")
            ganr = ', '.join(ganr1)
        else:
            ganr = 'Нет данных'
        if "countryOfOrigin" in data:
            country1 = data.get("countryOfOrigin")
            country = ', '.join(country1)
        else:
            country = 'Нет данных'
        logging.info('Информация о фильме собрана')
        return name, description, ocenka, img, ganr, country


def kino_main(url):
    parser = Kparser()
    data = parser.get_json(url)
    return parser.get_content(data)


if __name__ == '__main__':
    url = 'https://www.kinopoisk.ru/film/1262931/'
    kino_main(url)
