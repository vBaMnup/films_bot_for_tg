from random import choice


def get_random_user_agent():
    """Получаем случайные заголовки"""
    with open('../user_agents.txt', 'r') as user_agents_file:
        user_agents_list = [line.strip() for line in user_agents_file]

    return {
        'user-agent': choice(user_agents_list),
        'accept': '*/*'
    }
