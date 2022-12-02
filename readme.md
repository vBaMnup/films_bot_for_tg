# Проект Film bot for TG

[![films_bot workflow](https://github.com/vBaMnup/films_bot_for_tg/actions/workflows/films_bot.yml/badge.svg)](https://github.com/vBaMnup/films_bot_for_tg/actions/workflows/films_bot.yml)

[![Скриншот](https://github.
com/vBaMnup/films_bot_for_tg/blob/119b610faa6f0dffd4380378167762325cbb12f8
/img/film_bot.png)](https://t.me/funanekdot)

### Описание
Парсер новых фильмов на торрент трекере с возможностью постинга в телеграм-канал.
### Возможности

- Создание базы данных
- Парсинг трекера
- Парсинг google
- Получение информации о фильмах на кинопоиске
### Технологии

- Python 3.10
- beautifulsoup4
- PostgreSQL
- psycopg2
- telegram-bot-api

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

``` bash
git clone git@github.com:vBaMnup/api_final_yatube.git
```

```bash
cd films_bot_for_tg
```

Cоздать и активировать виртуальное окружение:

``` bash
python3 -m venv venv
```

``` bash
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:
``` bash
python3 -m pip install --upgrade pip
```

``` bash
pip install -r requirements.txt
```
Создать базу данных
```bash
python database/create_tables.py
```

Добавить в файл .env:
```python
TG_TOKEN='Токен телеграм-бота'
TG_NAME='@название канала'
```

Запустить проект:

``` bash
python main.py
```

### Пример работы
[Канал в Telegram](https://t.me/funanekdot)


### Автор
[Paskov Andrey](https://vk.com/andrey_paskov)