
class ApplicationConfiguration(object):
    """
        Flask application config.
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:111111@localhost/test'


class BotConfiguration(object):
    """
        Telegram bot config.
    """
    # TOKEN = r"527820020:AAGj3qIgb_cmkDWWIIXEC4w-cMR3pJ9QvRA"
    TOKEN = r"1836679393:AAHUCurIt8KUGEn4dvHJMqDDu4sJnnyC54U"


class ServerConfiguration(object):
    HOST = "https://4a7aa01f7880.ngrok.io"


class DBConfiguration(object):
    """
        Database connection config.
    """
    HOST = 'localhost'
    USER = 'postgres'
    PASS = '111111'
    DATABASE = 'test'
