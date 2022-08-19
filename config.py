import os
from dotenv import load_dotenv

# подготавливаемся к работе с dotenv
load_dotenv()

# сайт с прокси
PROXY_URL = os.getenv('PROXY_URL')

# База данных
DATABASE = os.getenv('DATABASE')

