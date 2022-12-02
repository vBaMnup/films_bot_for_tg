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
