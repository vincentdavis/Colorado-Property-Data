from peewee import MySQLDatabase
DB = MySQLDatabase('db_name',
                   user='DB_user',
                   password='db_Password',
                   host='DB_URL')