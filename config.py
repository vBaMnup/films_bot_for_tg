import logging
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

# Логирование
logging.basicConfig(level=logging.DEBUG)

# подготавливаемся к работе с dotenv
load_dotenv()

# сайт с прокси
PROXY_URL = os.getenv('PROXY_URL')

# База данных
# PATH =
DATABASE = os.getenv('DATABASE')

# Настройки трекера
TRACKER_DOMEN = os.getenv('TRACKER_DOMEN')
TRACKER_PARSING_URL = (
    os.getenv('TRACKER_PARSING_URL')
    + f'{datetime.strftime(datetime.now() - timedelta(days=1), "%d.%m.%Y")};'
      f'{datetime.strftime(datetime.now(), "%d.%m.%Y")}'
)

# Таймаут соединения
TIMEOUT = 5
