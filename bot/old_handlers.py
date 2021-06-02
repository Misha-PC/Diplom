from bot import teleBot
from database import db
from telebot import types


@teleBot.message_handler(commands=['start'])
@db.user
def start(message, user):
    """
    # /start

    # Need to user registration

    :param message: from "message_handler" decorator
    :param user: from "user" decorator
    :return: Void
    """
    if not user:
        db.create_user(message.chat.id)
    print(f"/start from {user}")


@teleBot.message_handler(commands=['sites'])
@db.user
def get_sites(message, user):
    """
    #   /sites

    #   Send Inline Keyboard Markup with all user sites.

    #   callback_data = "select:<id>"


    :param message: from "message_handler" decorator
    :param user: from "user" decorator
    :return: Void
    """

    sites = db.get_all_sites(user.id)
    if not sites:
        teleBot.send_message(message.chat.id, "У вас ещё нету сайтов. что бы создать введите '/new [название сайта]'.")
        return

    keyboard = types.InlineKeyboardMarkup()  # Клавиатура
    msg = 'Ваши сайты:\n'

    for site in sites:
        keyboard.add(types.InlineKeyboardButton(text=site.title, callback_data='select:' + str(site.id)))
        # msg += f"{site['id']}) {site['title']}: {site['url']}\n"

    teleBot.send_message(message.chat.id, text=msg, reply_markup=keyboard)


@teleBot.message_handler(commands=['new'])
@db.user
def new_sites(message, user):
    """
    #   /new [site title]

    #   Create and select new site.

    :param message: from "message_handler" decorator
    :param user: from "user" decorator
    :return: Void
    """

    if len(message.text) <= 5:
        teleBot.send_message(message.chat.id, "Да не так! етить колотить!")
        return

    title = message.text[5:]
    site = db.new_site(user.id, title)
    print("New site:", site)


@teleBot.message_handler(commands=['select'])
@db.user
def select_sites(message, user):
    """
    #   /select

    #   Deprecated!!!

    #   Select site to edit/delete.

    :param message: from "message_handler" decorator
    :param user: from "user" decorator
    :return: Void
    """

    code = message.text.split()
    if len(code) > 1:
        site_id = code[1]
        site = db.get_site(site_id=site_id, u_id=user.id)
        print(f"  ****Site: {site}")
        if site.member == message.text.id:
            db.select_site(user.id, site_id)
            msg = f'Выбрн сайт {site.head}. {HOST}site/{site.slug}'
        else:
            msg = 'Это не ваш сайт!'
    else:
        msg = 'Используйте /select <id>'

    teleBot.send_message(message.chat.id, msg)


@teleBot.message_handler(commands=['pin'])
def pin(message):
    """
    #   /pin

    #   Only test functions

    :param message: from "message_handler" decorator
    :return: Void
    """
    teleBot.pin_chat_message(message.chat.id, message.message_id)
    print('message id:' + str(message.message_id) + ' pinned.')
