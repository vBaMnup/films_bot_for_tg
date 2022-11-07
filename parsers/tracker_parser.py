
import logging
import time

import requests
from bs4 import BeautifulSoup

from config import TRACKER_DOMEN, TRACKER_PARSING_URL, TIMEOUT
from database.db_handler import Queue, Films
from kp_parser import kino_main
from tools.other import get_google_query
from tools.user_agent import get_random_user_agent


class ParserNoProxy:
    def __init__(self):
        self.queue = Queue()
        self.queue.clear_queue()

    def get_films(self) -> bool:
        """
        Получаю список новых фильмов на треккере
        :return:
        """
        while True:
            headers = get_random_user_agent()
            logging.info('Ищу новые фильмы в топе')
            try:
                req = requests.get(TRACKER_PARSING_URL,
                                   headers=headers,
                                   timeout=TIMEOUT).text
                logging.info('Получаю все ссылки')
                soup = BeautifulSoup(req, 'lxml')
                all_films = soup.findAll(True, {'class': ['gai', 'tum']})

                for film in all_films:
                    download = (film.findNext('td').findNext('td')
                                .findNext('a').findNext('a').get('href')
                                [:-35].replace("'", ""))
                    title = (film.findNext('a').findNext('a').findNext('a')
                             .text.replace("'", ""))
                    link = (TRACKER_DOMEN + film.findNext('a').findNext('a')
                            .findNext('a').get('href'))
                    self.queue.insert_to_database(title, link, download)
                return True
            except Exception as e:
                logging.error(f'Ошибка получения списка фильмов {e}')
                time.sleep(60)

    def get_next_film(self):
        self.get_films()
        film_id, title, tracker_link, download = self.queue.get_next_film_from_queue()
        return film_id, title, tracker_link, download

    def search_kplink_in_google(self, google_url, title):
        while True:
            logging.info(f'Ищу ссылку в гугле на {title}')
            headers = get_random_user_agent()
            try:
                req = requests.get(google_url,
                                   headers=headers,
                                   timeout=TIMEOUT)
                if req.status_code != 200:
                    logging.error(f'Ответ гугла {req.status_code}')
                else:
                    break
            except Exception as e:
                time.sleep(5)
                logging.error(e)
            finally:
                soup = BeautifulSoup(req.text, 'lxml')
                all_links = soup.findAll(class_='yuRUbf')
                if all_links:
                    for g_link in all_links:
                        link = g_link.findNext('a').get('href')
                        if 'google' in link:
                            continue
                        if link is None:
                            break
                        if '/film/' in link and 'kinopoisk' in link:
                            s = link.strip().split('/')
                            kino_link = f'{s[0]}//{s[2]}/{s[3]}/{s[4]}/'
                            logging.info(f'Ура: {kino_link}')
                            return kino_link
                logging.error('Отсутствует ссылка на кинопоиск, пробую еще...')
                time.sleep(30)


def main():
    a = ParserNoProxy()
    f = Films()
    q = Queue()
    film_id, title, link, download = a.get_next_film()
    if f.check_data_in_db('films', title, 'title'):
        f.insert_similar(title, download)
    else:
        google_query = get_google_query(title)
        kp_link = a.search_kplink_in_google(google_query, title)
        name, description, ocenka, img, ganr, country, year, actors = kino_main(kp_link)
        f.insert_to_films(title, description, float(ocenka), year, img, link,
                          kp_link, download, ganr, actors, country)
    q.change_handled(film_id)


if __name__ == '__main__':
    main()
