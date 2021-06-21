from telebot import types


actions = {
    'title': 'Название сайта',
    'head': 'Заголовок приветствия',
    'body': 'Приветствие',
    'about1': 'О себе',
    'about2': 'О товаре или услуге',
    'phone': 'Номер телефона',
    'email': 'Электронная почта',
    'loc': 'Адрес',
    'inst': 'Инстаграм',
    'vk1': 'Страница вк',
    'vk2': 'Группа вк',
    'facebook': 'Facebook',
    'twitter': 'Twitter',
    'tiktok': 'TikTok',
    # 'photo1': 'Фотография главной страницы',
    # 'photo2': 'Фотография страницы "О себе"',
    # 'photo3': 'Фотография страницы "О товаре(услуге)"'
}


def action_to_code(name):
    code = 1
    for i in actions.keys():
        if name == i:
            return code
        code += 1
    return -1


def code_to_action(code):
    current = 1
    for i in actions.keys():
        if current == code:
            return i
        current += 1
    return -1


def dict_to_keyboard(keys, name):
    keyboard = types.InlineKeyboardMarkup()

    for item in keys.items():
        code, text = item
        keyboard.add(types.InlineKeyboardButton(text=str(text), callback_data=f"{name}:{code}"))

    return keyboard


ACTION_KEYBOARD = dict_to_keyboard(actions, 'action')


