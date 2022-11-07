import logging
import psycopg2
from datetime import datetime
from time import time

from peewee import (PostgresqlDatabase, Model, CharField,
                    DateField, BooleanField, FloatField)

from config import user, password, host, db_name


class Queue:
    def __init__(self):
        self.user = user
        self.password = password
        self.host = host
        self.db_name = db_name

    def connection_to_db(self):
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
        except Exception as _ex:
            print('[INFO] Error while working with PSQL', _ex)
        return connection

    def insert_to_database(self, title, url, download):
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                f"""
                    INSERT INTO queue (title, link, download, handled)
                    VALUES ('{title}', '{url}', '{download}', FALSE)
                """
            )
            logging.debug(f'Фильм {title} добавлен в базу данных')

    def get_next_film_from_queue(self):
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                """
                    SELECT title, link, download
                    FROM queue
                    WHERE handled = FALSE
                    LIMIT 1;
                """
            )
            return cursor.fetchone()

    def clear_queue(self):
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                f"""
                    DELETE FROM queue
                """
            )



# psql_db = PostgresqlDatabase(
#     db_name,
#     user=user
# )
#
#
# class BaseModel(Model):
#     class Meta:
#         database = psql_db
#
#
# class Films(ModelBase):
#     name = CharField()
#     description = CharField()
#     review = FloatField()
#     poster = CharField()
#     tracker_url = CharField()
#     ganr = CharField()
#     country = CharField()
#     kinopoisk_url = CharField()
#     download = CharField()
#     parse_date = DateField()
#     posted = BooleanField()
#     similar_films = CharField(null=True)
#
#
# def check_db_tracker(url):
#     logging.info('Проверяю ссылку на треккер в базе')
#     return Films.select().where(Films.tracker_url == url).exists()
#
#
# def check_db_kp(url):
#     logging.info('Проверяю ссылку на кп в базе')
#     return Films.select().where(Films.kinopoisk_url == url).exists()
#
#
# def save_db(url, name, description, review, poster, tracker_url, download, ganr, country):
#     if url:
#         film_new = Films(name=name,
#                          description=description,
#                          review=review,
#                          poster=poster,
#                          tracker_url=tracker_url,
#                          ganr=ganr,
#                          country=country,
#                          kinopoisk_url=url,
#                          download=download,
#                          parse_date=datetime.strftime(datetime.now(),
#                                                       "%d.%m.%Y"),
#                          posted=False)
#         film_new.save()
#         logging.info('Сохраняю фильм в базу')
#
#
# def add_similar_films(url_kp, name, download):
#     logging.info('Поиск похожих фильмов')
#     if Films.select().where(Films.kinopoisk_url == url_kp).exists():
#         logging.info('Фильм есть в базе')
#         film = Films.get(Films.kinopoisk_url == url_kp)
#         if film.similar_films is None:
#             logging.info('Создаю список похожих')
#             try:
#                 Films.update(
#                     similar_films=Films.similar_films
#                     + f'{name} {download}|'
#                 ).where(Films.kinopoisk_url == url_kp).execute()
#             except Exception as e:
#                 print(e)
#             logging.info('Фильм добавлен в список похожих')
#         elif name not in film.similar_films:
#             logging.info('Пробую добавить в похожие')
#             Films.update(
#                 similar_films=Films.similar_films
#                 + f'{name} {download}|'
#             ).where(Films.kinopoisk_url == url_kp).execute()
#             logging.info('Сохраняю список похожих фильмов')
#         else:
#             logging.info('Фильм есть в списке')
#
#

if __name__ == '__main__':
    title = 'Поехали! / En roue libre (2022) WEB-DL 1080p от селезень | D'
    url = 'http://rutor.info/torrent/894705/poehali!_en-roue-libre-2022-web-dl-1080p-ot-selezen-d'
    download = 'magnet:?xt=urn:btih:b8c7bb418aa14458f4aaefb399451f172a1eaa75&dn=rutor.info_%D0%9F%D0%BE%D0%B5%D1%85%D0%B0%D0%BB%D0%B8%21+%2F+En+roue+libre+%282022%29+WEB-DL+1080p+%D0%BE%D1%82+%D1%81%D0%B5%D0%BB%D0%B5%D0%B7%D0%B5%D0%BD%D1%8C+%7C+D&tr=udp://opentor.net:6969&tr=http://retracker.local/announce'
    p = Queue()
    p.insert_to_database(title, url, download)
