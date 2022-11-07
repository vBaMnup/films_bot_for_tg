import logging
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

# Логирование
logging.basicConfig(level=logging.INFO)

# подготавливаемся к работе с dotenv
load_dotenv()

# Нужно ли использовать прокси
proxy = os.getenv('USE_PROXY')

# сайт с прокси
PROXY_URL = os.getenv('PROXY_URL')

# База данных
DATABASE = os.getenv('DATABASE')

# Настройки трекера
GOOGLE_URL = os.getenv('GOOGLE_URL')
TRACKER_DOMEN = os.getenv('TRACKER_DOMEN')
TRACKER_PARSING_URL = (
    os.getenv('TRACKER_PARSING_URL')
    + f'{datetime.strftime(datetime.now() - timedelta(days=1), "%d.%m.%Y")};'
      f'{datetime.strftime(datetime.now(), "%d.%m.%Y")}'
)

# Таймаут соединения
TIMEOUT = 2

# Данные подключения к базе Postgres
host = os.getenv('PG_HOST')
user = os.getenv('PG_USER')
password = os.getenv('PG_PASSWORD')
db_name = os.getenv('PG_DATABASE')
