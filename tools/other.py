import logging


def get_title(content):
    """
    Получение тайтла
    :param content:
    :return:
    """
    logging.info(content)
    return content.xpath('//body//h1/text()')[0]


def get_google_query(title: str) -> str:
    """
    Создание запроса в гугл
    :param title:
    :return:
    """
    if not title:
        assert Exception('Пустой тайтл')
    title_split: list = title.split('(')
    header: list = title_split[0].strip().split(" / ")
    if len(header) >= 2:
        return (
            f'https://www.google.com/search?'
            f'q=кинопоиск+{header[0]}+{header[1]}'
        )
    return f'https://www.google.com/search?q=кинопоиск+{title_split}'


def make_link(string: str) -> str:
    s: list = string.strip().split('/')
    kino_link: str = f'{s[0]}//{s[2]}/{s[3]}/{s[4]}/'
    return kino_link


def make_text(title: str, ganre: str, country: str, description: str,
              ocenka: str) -> str:
    text: str = (f'<b>{title}</b>\n<b>Жанр</b>: {ganre}\n<b>Страна</b>: '
                 f'{country}\nОписание:\n <i>{description}</i>\n\nОценка '
                 f'кинопоиск: {ocenka}\n\n')
    return text


def check_text_to_wright_len(title: str, ganre: str, country: str,
                             description: str, ocenka: str) -> str:
    text: str = make_text(title, ganre, country, description, ocenka)
    len_text: int = len(text)
    if len_text <= 1024:
        return text
    difference = len_text - 1024
    description = description[0:-difference]
    text: str = make_text(title, ganre, country, description, ocenka)
    return text
