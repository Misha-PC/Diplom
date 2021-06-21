from bot import teleBot
from database import db
from bot.keyboards import actions
from telebot import types
from bot.keyboards import action_to_code
from bot.keyboards import actions
from bot.keyboards import code_to_action


@teleBot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """
    # This function handles the whole keyboard

    # select:<id>

    # del:<id>

    :param call: from "callback_query_handler" decorator
    :return: Void
    """
    def select(tg_id, site_id):
        user = db.get_user(tg_id=tg_id, r=True)
        db.select_site(user.id, site_id)
        site = db.get_site(site_id=site_id)
        href = 'https://366e8d8c7552.ngrok.io'
        teleBot.send_message(tg_id, f"Выбран сайт '{site.title}.' {href}/site/{site.slug}")
        print(user)
        print(f"User '{tg_id}' select site '{site_id}'")

    def remove(tg_id, site_id):
        print(f"User '{tg_id}' delete site '{site_id}'")

    def action(tg_id, action_name):
        action_code = action_to_code(action_name)
        db.set_user_status(action_code, tg_id=tg_id)
        teleBot.send_message(tg_id, f'Введите "{actions[action_name]}":')
        print(f"from user '{tg_id} set status {action_code}: {action_name}'")

    if ":" not in call.data:
        return
    code, value = call.data.split(":")
    handler_list = {
        'select': select,
        'del': remove,
        'action': action
    }
    handler_list[code](call.message.chat.id, value)
    print(call.data)
    teleBot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
