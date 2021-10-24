from flask_mysqldb import MySQL

class Config():
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "test"
    MYSQL_DB = "trabbd"

config = {"gabconfig":Config()}