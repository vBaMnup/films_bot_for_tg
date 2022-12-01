'''
TODO:
+ Подключить бота
- Получить данные о фильме из базы (если он еще не публиковался
  и у него есть постер)
- Распарсить данные
- Отправить сообщение в тг
- Отдельный поток ищет фильмы (30 минут)
  и отправляет сообщение (60 минут)
- сообщения отправляются с 6:00 до 23:59
'''
from asyncio import sleep as asleep

import telebot
from config import TOKEN, CHANNEL_NAME
from parsers.tracker_parser import main as search_main

bot = telebot.TeleBot(TOKEN)
channel = CHANNEL_NAME


def get_data_from_db():
    pass


def format_data(data):
    pass


def send_message():
    pass


async def serch_films():
    search_main()
    await asleep(1800)


def main():
    pass


if __name__ == '__main__':
    main()
