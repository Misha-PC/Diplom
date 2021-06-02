from bot import teleBot
from database import db
from bot.keyboards import ACTION_KEYBOARD
from bot.keyboards import dict_to_keyboard
from telebot import types

HOST = "localhost:5000/"


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
    teleBot.send_message(message.chat.id, "Что бы создать сайт напишите /new")
    print(f"/start from {user}")


@teleBot.message_handler(commands=['new'])
@db.user
def new_site(message, user):
    """
    #   /new [site title]

    #   Create and select new site.

    :param message: from "message_handler" decorator
    :param user: from "user" decorator
    :return: Void
    """
    if len(message.text) <= 5:
        db.set_user_status(-1, user.id)
        teleBot.send_message(message.chat.id, "Введите название сайта")
        return

    title = message.text[5:]
    site = db.new_site(user.id, title)
    href = 'https://366e8d8c7552.ngrok.io'
    msg = f'Создан сайт {site.title}. Вот ссылочка: {href}/site/{site.slug}'
    teleBot.send_message(message.chat.id, text=msg, reply_markup=ACTION_KEYBOARD)
    print("New site:", site)


@teleBot.message_handler(commands=['status'])
@db.user
def get_status(message, user):
    if len(message.text) > 7:
        db.set_user_status(message.text[7:], user.id)
        return
    teleBot.send_message(message.chat.id, f'Status code: {user.status}')


@teleBot.message_handler(commands=['mysites'])
@db.user
def get_status(message, user):
    data = {}
    sites = db.get_all_sites(user.id)

    for site in sites:
        data.update({site.id: site.title})
    keyboard = dict_to_keyboard(data, 'select')

    teleBot.send_message(message.chat.id, f'Select site:', reply_markup=keyboard)


@teleBot.message_handler(commands=['select'])
@db.user
def get_status(message, user):
    if len(message.text) > 7:
        db.select_site(user.id, message.text[7:])
        teleBot.send_message(message.chat.id, f'Site #{message.text[7:]} selected')
        return

    teleBot.send_message(message.chat.id, f'Site #{user.selected} selected')


@teleBot.message_handler(commands=['set'])
@db.user
def get_status(message, user):
    teleBot.send_message(message.chat.id, text='Выберите действие:', reply_markup=ACTION_KEYBOARD)
