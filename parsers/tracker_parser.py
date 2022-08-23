
import logging
import time

from requests_html import HTMLSession

from config import TRACKER_DOMEN, TRACKER_PARSING_URL, TIMEOUT
from database.db_handler import check_db_tracker, add_similar_films, save_db
from tools.other import get_title, get_google_query
from tools.proxy import get_proxies
from tools.user_agent import get_random_user_agent
from kp_parser import kino_main, LIST_BAD_PROXY


class Parser:
    def __init__(self):
        self.session = HTMLSession()

    def check_proxy(self):
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
                request = self.session.get(TRACKER_DOMEN,
                                           headers=get_random_user_agent(),
                                           proxies=random_proxy,
                                           timeout=TIMEOUT)
                if request.status_code != 200:
                    LIST_BAD_PROXY.add(proxy)
                    assert Exception(f'Прокси "{random_proxy}" '
                                     f'вернул не верный статус-код')
                LIST_BAD_PROXY.add(proxy)
                logging.info(f'Найден рабочий прокси: {random_proxy}')
                return random_proxy
            except Exception:
                LIST_BAD_PROXY.add(proxy)
                logging.error(f'Прокси {random_proxy} не смог подключиться')

    def get_films(self):
        """
        Получаю список фильмов в топе на трекере
        :return: Список ссылок
        """
        while True:
            try:
                logging.info('Ищу новые фильмы в топе')
                request = self.session.get(TRACKER_PARSING_URL,
                                           headers=get_random_user_agent(),
                                           proxies=self.check_proxy(),
                                           timeout=TIMEOUT)
                logging.info('Получаю все ссылки')
                content_links = request.html.xpath("//table[1]//a[3]/@href")
                links = []
                for i, link in enumerate(content_links):
                    if i < 12:
                        links.append(TRACKER_DOMEN + link)
                logging.info('Собрал список новых фильмов')
                logging.debug(links)
                if links:
                    logging.info('Собрал список новых фильмов')
                    return links
                logging.debug('Пустой список ссылок')
            except Exception:
                logging.error('Ошибка получения списка фильмов')

    def get_film_page(self, url):
        """
        Получаем html страницы с фильмом
        :param url: ссылка на фильм на трекере
        :return: html
        """
        logging.info('Получаю контент со страницы фильма')
        while True:
            try:
                new_proxy = self.check_proxy()
                request = self.session.get(url,
                                           headers=get_random_user_agent(),
                                           proxies=new_proxy,
                                           timeout=TIMEOUT)
                return request.html
            except Exception as e:
                logging.critical(e)
                logging.error('Не удалось получить контент со страницы '
                              'фильма')

    def search_kplink_in_google(self, google_url, title):
        """
        Обработчик поиска ссылки на фильм в гугле
        :param google_url: Запрос в гугл
        :param title: Название фильма на трекере
        :return: Ссылка на кинопоиск
        """
        while True:
            while True:
                try:
                    logging.info(fr'Ищу ссылку в гугле на {title}')
                    request = self.session.get(
                        google_url,
                        headers=get_random_user_agent()
                    )
                    if request.status_code != 200:
                        logging.error(f'Ответ гугла {request.status_code}')
                    else:
                        break
                except Exception as e:
                    time.sleep(5)
                    logging.error(e)
            g_links = request.html.xpath('//*[@id="rso"]//a/@href')
            if g_links:
                for g_link in g_links:
                    if 'google' in g_link:
                        continue
                    if g_link == None:
                        break
                    if 'kinopoisk' in g_link and 'film' in g_link:
                        s = g_link.strip().split('/')
                        kino_link = f'{s[0]}//{s[2]}/{s[3]}/{s[4]}/'
                        logging.info(f'Ура: {kino_link}')
                        return kino_link
            logging.error('Отсутствует ссылка на кинопоиск, пробую еще...')
            time.sleep(30)

    def get_kp_link_from_google(self, link):
        """
        Ищу в гугле ссылку на кинопоиск по выбранному фильму
        :param link: ссылка на фильм на трекере
        :return: ссылку на кинопоиск
        """
        content = self.get_film_page(link)
        title = get_title(content)
        google_url = get_google_query(title)
        kp_link = self.search_kplink_in_google(google_url, title)
        download = content.xpath('//*[@id="download"]/a[1]/@href')[0]
        logging.info(f'Поиск "{link}" в базе данных')
        if not check_db_tracker(link):
            logging.info(f'{link} нет в базе')
            return kp_link, title, download
        logging.info('Есть в базе')
        add_similar_films(kp_link, title, download)

    def save_film(self, url):
        """
        Созраняет фильм в базу
        :param url: Ссылка на трекер
        :return:
        """
        g_link = self.get_kp_link_from_google(url)
        if g_link:
            result = kino_main(g_link[0])
            name = g_link[1]
            description = result[1]
            ocenka = float(result[2])
            poster = 'https:' + result[3]
            ganr = result[4]
            country = result[5]
            stranica_rutor = url
            download = g_link[2][0: -35]
            save_db(g_link[0], name, description, ocenka, poster,
                    stranica_rutor, download, ganr, country)


def main():
    parser_tracker = Parser()
    film_list_url = parser_tracker.get_films()
    for link in film_list_url:
        parser_tracker.save_film(link)


def main2():
    parser_tracker = Parser()
    url = 'http://rutor.info/torrent/885407/top-gan-mjeverik_top-gun-maverick-2022-web-dl-1080p-ot-selezen-p-imax'
    parser_tracker.save_film(url)


# p = Parser()
# films = p.get_films()
# print(f'{len(films)}: {films}')
# print(p.get_kp_link_from_google('http://rutor.info/torrent/885241/bystree-puli_bullet-train-2022-ts-avc-d'))
# print(check_db_tracker('http://rutor.info/torrent/885241/bystree-puli_bullet-train-2022-ts-avc-d'))
# print(p.save_film('http://rutor.info/torrent/885241/bystree-puli_bullet-train-2022-ts-avc-d'))
if __name__ == '__main__':
    main2()
