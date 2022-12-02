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
from asyncio import sleep as asleep

import telebot

from config import CHANNEL_NAME, TOKEN
from database.db_handler import Films
from parsers.tracker_parser import main as search_main

bot = telebot.TeleBot(TOKEN)
channel = CHANNEL_NAME


def get_data_from_db():
    f = Films()
    data_list: list = f.get_film_from_db()
    ganrs: list = f.get_ganre_by_id(data_list[0])
    countries: list = f.get_country_by_id(data_list[0])
    return data_list, ganrs, countries


def format_data(data):
    pass


def send_message():
    pass


async def clear_db():
    pass


async def serch_films():
    search_main()
    await asleep(1800)


def main():
    print(*get_data_from_db())


if __name__ == '__main__':
    main()
