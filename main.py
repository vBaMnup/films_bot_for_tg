'''
TODO:
+ Подключить бота
- Получить данные о фильме из базы (если он еще не публиковался
  и у него есть постер)
- Распарсить данные
- Отправить сообщение в тг
+ Отдельный поток ищет фильмы (30 минут)
- и отправляет сообщение (60 минут)
- сообщения отправляются с 6:00 до 23:59
'''
import asyncio
import time
from asyncio import sleep as asleep

import telebot

from config import CHANNEL_NAME, TOKEN
from database.db_handler import Films
from parsers.tracker_parser import main as search_main
from tools.other import check_text_to_wright_len

BOT = telebot.TeleBot(TOKEN)
FILMS_DB = Films


def get_data_from_db():
    data_list: list = FILMS_DB.get_film_from_db()
    ganrs: list = FILMS_DB.get_ganre_by_id(data_list[0])
    countries: list = FILMS_DB.get_country_by_id(data_list[0])
    return data_list, ganrs, countries


def format_data(data):
    data, ganres, countries = get_data_from_db()
    id = data[0]
    poster_url: str = data[4]
    title: str = data[1]
    ganre = ', '.join(map(str, ganres))
    country = ', '.join(map(str, countries))
    description: str = data[2]
    ocenka: str = data[3] if data[3] != 0.0 else 'Без оценки'
    download: str = data[-1]
    text = check_text_to_wright_len(title, ganre, country, description,
                                    ocenka)
    download_text = f'Скачать:\n <i>{download}</i>\n'
    return id, text, poster_url, download_text


def send_message(id: int, text: str, poster: str, download: str) -> None:
    BOT.send_photo(CHANNEL_NAME, poster, caption=text, parse_mode='HTML')
    time.sleep(10)
    BOT.send_message(CHANNEL_NAME, download, parse_mode='HTML')
    FILMS_DB.change_posted(id)


def clear_db():
    pass


async def search_films():
    while True:
        search_main()
        await asleep(1800)


async def main():
    while True:
        data = get_data_from_db()
        id, text, poster, download = format_data(data)
        send_message(id, text, poster, download)
        await asleep(3600)


if __name__ == '__main__':
    while True:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(search_films()),
            loop.create_task(main())
        ]
        wait_tasks = asyncio.wait(tasks)
        loop.run_until_complete(wait_tasks)
        loop.close()
