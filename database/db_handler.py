import logging
import psycopg2
from datetime import datetime

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
                    SELECT id, title, link, download
                    FROM queue
                    WHERE handled = FALSE
                    LIMIT 1;
                """
            )
            return cursor.fetchone()

    def change_handled(self, id):
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                f"""
                    UPDATE queue
                    SET handled = TRUE
                    WHERE id = {id}
                """
            )

    def clear_queue(self):
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                f"""
                    DELETE FROM queue
                """
            )


class Films:
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

    def check_data_in_db(self, db_name, data, column):
        try:
            with self.connection_to_db().cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT {column}
                        FROM {db_name}
                        WHERE {column} = '{data}'
                    """
                )
                result = cursor.fetchone()[0]
                return result == data
        except TypeError:
            return False

    def insert_to_mediator(self, db_mediator_name, db2_name,
                           name_mediator2, id_name2,
                           column_name2, data1, data2):
        with self.connection_to_db().cursor() as cursor:
            cursor.execute(
                f"""
                    INSERT INTO {db_mediator_name} (film_id, {name_mediator2})
                    VALUES ((SELECT id FROM films WHERE title = '{data1}'),
                        (SELECT {id_name2} FROM {db2_name} WHERE {column_name2} = '{data2}'))
                """
            )
            logging.info('Таблица Mediator дополнена')

    def insert_to_films(self, title, description, ocenka, year, poster,
                        tracker_page, kino_page, download, ganres, actors,
                        countries):
        self.insert_to_table('ganre', 'ganre_name', ganres)
        self.insert_to_table('actors', 'name', actors)
        self.insert_to_table('country', 'country', countries)
        if not self.check_data_in_db('films', title, 'title'):
            with self.connection_to_db().cursor() as cursor:
                cursor.execute(
                    f"""
                        INSERT INTO films (title,
                            description,
                            ocenka,
                            year,
                            poster,
                            tracker_page,
                            kino_page,
                            download)
                        VALUES ('{title}', '{description}', '{ocenka}', '{year}',
                                '{poster}', '{tracker_page}', '{kino_page}', '{download}')
                    """
                )
                logging.debug(f'Фильм {title} добавлен в базу данных')
            for ganre in ganres:
                self.insert_to_mediator('film_ganre', 'ganre', 'ganre_id', 'ganre_id',
                                        'ganre_name', title, ganre)
            for actor in actors:
                self.insert_to_mediator('film_actors', 'actors', 'actors_id',
                                        'actors_id', 'name', title, actor)
            for country in countries:
                self.insert_to_mediator('film_country', 'country', 'country_id',
                                        'country_id', 'country', title, country)
        else:
            logging.info('Фильм уже есть в базе')

    def insert_to_table(self, db_name, column_name, arr):
        try:
            with self.connection_to_db().cursor() as cursor:
                for item in arr:
                    if self.check_data_in_db(db_name, item, column_name):
                        logging.info(f'Жанр {item} уже есть в базе')
                        continue
                    cursor.execute(
                        f"""
                            INSERT INTO {db_name} ({column_name})
                            VALUES ('{item}')
                        """
                    )
        except Exception as _e:
            logging.error(f'Ошибка добавления значения: {_e}')

    def insert_similar(self, title, download):
        try:
            if not self.check_data_in_db('similar_films', title, 'title'):
                with self.connection_to_db().cursor() as cursor:
                    cursor.execute(
                        f"""
                            INSERT INTO similar_films (film_id, title, download)
                            VALUES ((SELECT id FROM films WHERE title LIKE '{title.split(')')[0]}%'), '{title}', '{download}')
                        """
                    )
            else:
                logging.info(f'Фильм {title} уже есть в списке похожих')
        except Exception as _e:
            logging.error(f'Ошибка добавления значения: {_e}')
