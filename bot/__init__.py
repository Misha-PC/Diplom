import telebot
from config import BotConfiguration

"""
    Create telebot exemplar. 
"""

teleBot = telebot.TeleBot(BotConfiguration.TOKEN)


"""
    Init handlers
"""
import bot.callback_handlers
import bot.command_handlers
import bot.text_handlers
