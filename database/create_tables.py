"""
TODO:
Таблицы:
Фильмы +-
Жанры +
Жанры-фильмы +
Страны +
Страны-фильмы +
Актеры +
Актеры-Фильмы +
Похожие фильмы -
Жанры, страны, актеры Уникальны +
"""

import logging

import psycopg2

from config import db_name, host, password, user


class Table:
    def __init__(self):
        self.host = host
        self.password = password
        self.host = host
        self.db_name = db_name

    def connection_to_db(self):
        """Подключаемся к базе данных"""
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
        except Exception as _ex:
            logging.error('Error while working with PSQL', _ex)
            return _ex
        return connection

    def create_table_queue(self):
        """Создаем очередь"""
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                """
                    CREATE TABLE queue(id serial PRIMARY KEY,
                    title VARCHAR(1000),
                    link VARCHAR(1000),
                    download VARCHAR(1000),
                    handled BOOLEAN NOT NULL);
                """
            )
        logging.info('Таблица Queue успешно создана')

    def create_ganre(self):
        """Создаем таблицу жанров"""
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                '''
                    CREATE TABLE ganre (
                    ganre_id serial PRIMARY KEY,
                    ganre_name VARCHAR(50) NOT NULL UNIQUE
                    )
                '''
            )
        logging.info('Таблица Ganre успешно создана')

    def create_country(self):
        """Создаем таблицу стран"""
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                '''
                    CREATE TABLE country (
                    country_id serial PRIMARY KEY,
                    country VARCHAR(50) NOT NULL UNIQUE
                    )
                '''
            )
        logging.info('Таблица Country успешно создана')

    def create_actors(self):
        """Создаем таблицу стран"""
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                '''
                    CREATE TABLE actors (
                    actors_id serial PRIMARY KEY,
                    name VARCHAR(50) NOT NULL UNIQUE
                    )
                '''
            )
        logging.info('Таблица actors успешно создана')

    def create_films(self):
        """Создаем таблицу фильмов"""
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                '''
                    CREATE TABLE films (
                    id serial PRIMARY KEY,
                    title VARCHAR(150) NOT NULL,
                    description TEXT,
                    ocenka NUMERIC(2,1),
                    year INT,
                    poster VARCHAR(150) NOT NULL,
                    tracker_page VARCHAR(255) NOT NULL,
                    kino_page varchar(50) NOT NULL,
                    download TEXT NOT NULL,
                    parse_date DATE NOT NULL DEFAULT CURRENT_DATE,
                    posted BOOLEAN DEFAULT FALSE
                );'''
            )
        logging.info('Таблица Films успешно создана')

    def create_film_ganre(self):
        """Создаем вспомогательную таблицу фильм-жанр"""
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                '''
                    CREATE TABLE film_ganre (
                        film_id INT,
                        ganre_id INT,
                        FOREIGN KEY(film_id) REFERENCES films(id),
                        FOREIGN KEY(ganre_id) REFERENCES ganre(ganre_id)
                    )
                '''
            )
        logging.info('Таблица film_ganre успешно создана')

    def create_film_country(self):
        """Создаем вспомогательную таблицу фильм-страна"""
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                '''
                    CREATE TABLE film_country (
                        film_id INT,
                        country_id INT,
                        FOREIGN KEY(film_id) REFERENCES films(id),
                        FOREIGN KEY(country_id) REFERENCES country(country_id)
                    )
                '''
            )
        logging.info('Таблица film_country успешно создана')

    def create_film_actors(self):
        """Создаем вспомогательную таблицу фильм-актер"""
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                '''
                    CREATE TABLE film_actors (
                        film_id INT,
                        actors_id INT,
                        FOREIGN KEY(film_id) REFERENCES films(id),
                        FOREIGN KEY(actors_id) REFERENCES actors(actors_id)
                    )
                '''
            )
        logging.info('Таблица film_actors успешно создана')

    def create_similar_films(self):
        """Создаем вспомогательную таблицу похожих фильмов"""
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                '''
                    CREATE TABLE similar_films (
                        id serial PRIMARY KEY,
                        film_id INT,
                        title VARCHAR(150) UNIQUE,
                        download TEXT NOT NULL,
                        FOREIGN KEY (film_id) REFERENCES films(id)
                    )
                '''
            )
        logging.info('Таблица similar_films успешно создана')

    def drop_all(self):
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                """
                    DROP TABLE film_actors;
                    DROP TABLE film_country;
                    DROP TABLE film_ganre;
                    DROP TABLE similar_films;
                    DROP TABLE actors;
                    DROP TABLE country;
                    DROP TABLE films;
                    DROP TABLE ganre;
                    DROP TABLE queue;
                """
            )
            logging.info('Все таблицы уничтожены')


if __name__ == '__main__':
    create_tables = Table()
    create_tables.connection_to_db()
    create_tables.create_table_queue()
    create_tables.create_ganre()
    create_tables.create_country()
    create_tables.create_actors()
    create_tables.create_films()
    create_tables.create_film_ganre()
    create_tables.create_film_country()
    create_tables.create_film_actors()
    create_tables.create_similar_films()
    # create_tables.drop_all()
