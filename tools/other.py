def get_title(content):
    """
    Получаем полное название фильма
    :param content: Контент страницы фильма
    :return: название
    """
    return content.xpath('//body//h1/text()')


def get_google_query(title):
    """
    Создаем запрос в гугл из полного названия фильма
    :param title:
    :return:
    """
    title_split = title[0].strip().split('(')
    header = title_split[0].strip().split(" / ")
    if len(header) >= 2:
        return (
            f'https://www.google.com/search?'
            f'q=кинопоиск+{header[0]}+{header[1]}'
        )
    return f'https://www.google.com/search?q=кинопоиск+{title_split}'
