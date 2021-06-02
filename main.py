from threading import Thread
from app import webApp
from bot import teleBot
from database import db

if __name__ == "__main__":
    bot_thread = Thread(target=teleBot.polling)
    bot_thread.start()
    webApp.run()
