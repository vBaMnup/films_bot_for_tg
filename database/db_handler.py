import logging
from datetime import datetime

from peewee import (SqliteDatabase, Model, CharField,
                    DateField, BooleanField, FloatField)

from config import DATABASE

db = SqliteDatabase(DATABASE)


class ModelBase(Model):
    class Meta:
        database = db


class Films(ModelBase):
    name = CharField()
    description = CharField()
    review = FloatField()
    poster = CharField()
    tracker_url = CharField()
    ganr = CharField()
    country = CharField()
    kinopoisk_url = CharField()
    download = CharField()
    parse_date = DateField()
    posted = BooleanField()
    similar_films = CharField(null=True)


def check_db_tracker(url):
    logging.info('Проверяю ссылку на треккер в базе')
    return Films.select().where(Films.tracker_url == url).exists()


def check_db_kp(url):
    logging.info('Проверяю ссылку на кп в базе')
    return Films.select().where(Films.kinopoisk_url == url).exists()


def save_db(url, name, description, review, poster, tracker_url, download, ganr, country):
    if url:
        film_new = Films(name=name,
                         description=description,
                         review=review,
                         poster=poster,
                         tracker_url=tracker_url,
                         ganr=ganr,
                         country=country,
                         kinopoisk_url=url,
                         download=download,
                         parse_date=datetime.strftime(datetime.now(),
                                                      "%d.%m.%Y"),
                         posted=False)
        film_new.save()
        logging.info('Сохраняю фильм в базу')


def add_similar_films(url_kp, name, download):
    logging.info('Поиск похожих фильмов')
    if Films.select().where(Films.kinopoisk_url == url_kp).exists():
        film = Films.get(Films.kinopoisk_url == url_kp)
        if name not in film.similar_films:
            Films.update(
                similar_films=Films.similar_films
                + f'{name} {download}|'
            ).where(Films.kinopoisk_url == url_kp).execute()
            logging.info('Сохраняю список похожих фильмов')
        logging.info('Фильм есть в списке')


if __name__ == '__main__':
    Films.create_table()
    # print(check_db_tracker('http://rutor.info/torrent/885241/bystree-puli_bullet-train-2022-ts-avc-d'))