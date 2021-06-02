"""

    Status list:
        0) No status
        1) Expected site title
        2) Expected head text
        3) Expected body text
        4) Expected side bar
        5) Expected footer text
        6) Expected photo
        7) Expected background photo

"""
from bot import teleBot
from database import db
from bot.keyboards import ACTION_KEYBOARD
from bot.keyboards import code_to_action
from datetime import datetime
from telebot import types


@teleBot.message_handler(content_types=['text'])
@db.user
def text(message, user=None):
    """

    #   This processor is intended for all user text messages

    #   Processing based from user.status

    :param message: from message_handler decorator
    :param user: from db.user decorator
    :return: Void
    """

    def clear_status(user_id):
        db.set_user_status(0, user_id)
        return True

    if not user:
        teleBot.send_message(message.chat.id, "Для использования бота необходимо зарегистрироваться /start.")
        return

    if user.status < 1:
        if user.status == -1:
            site = db.new_site(user.id, message.text)
            href = 'https://366e8d8c7552.ngrok.io'
            db.select_site(user.id, site.id)
            teleBot.send_message(message.chat.id,
                                 f"Создан сайт {site.title}. Вот ссылочка: {href}/site/{site.slug}",
                                 reply_markup=ACTION_KEYBOARD)
            return
        teleBot.send_message(message.chat.id, "И куда это записывать? Выберите действие! /")
        return

    column = code_to_action(user.status)
    teleBot.send_message(message.chat.id, f"Успешно! Можете вызвать меню /set ещё раз или "
                                          f"воспользоваться предыдущим для продолжения работы с сайтом ")

    if column == -1 or not column:
        teleBot.send_message(message.chat.id, "Неизвестная ошибка сервера.")
        return

    def prepear_text(text):
        return text.replace('$', ':dol:')

    data = {
        column: prepear_text(message.text),
        'last_update': datetime.now()
    }

    db.update_site_data(user.selected, **data)

    # teleBot.send_message(message.chat.id)


