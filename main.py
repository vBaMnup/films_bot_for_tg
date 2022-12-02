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
from asyncio import sleep as asleep

import telebot

from config import CHANNEL_NAME, TOKEN
from database.db_handler import Films
from parsers.tracker_parser import main as search_main
from tools.other import check_text_to_wright_len
import time

bot = telebot.TeleBot(TOKEN)
channel = CHANNEL_NAME


def get_data_from_db():
    f = Films()
    data_list: list = f.get_film_from_db()
    ganrs: list = f.get_ganre_by_id(data_list[0])
    countries: list = f.get_country_by_id(data_list[0])
    return data_list, ganrs, countries


def format_data(data):
    data, ganres, countries = get_data_from_db()
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
    return text, poster_url, download_text


def send_message(text: str, poster: str, download: str) -> None:
    bot.send_photo(CHANNEL_NAME, poster, caption=text, parse_mode='HTML')
    time.sleep(10)
    bot.send_message(CHANNEL_NAME, download, parse_mode='HTML')


async def clear_db():
    pass


async def serch_films():
    search_main()
    await asleep(1800)


def main():
    data = get_data_from_db()
    # print(*data)
    # print(format_data(data))
    # print(len(format_data(data)))
    text, poster, download = format_data(data)
    send_message(text, poster, download)


if __name__ == '__main__':
    main()
