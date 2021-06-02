from database.db_object import Database
from config import DBConfiguration

"""
    Create new connection.
"""
db = Database(
    dbname=DBConfiguration.DATABASE,
    host=DBConfiguration.HOST,
    user=DBConfiguration.USER,
    password=DBConfiguration.PASS
)
