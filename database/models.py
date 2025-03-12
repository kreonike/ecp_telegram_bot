import os
from peewee import SqliteDatabase, Model, IntegerField, TextField, DateTimeField
import datetime

DATABASE_DIR = 'database'
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)
db = SqliteDatabase(os.path.join(DATABASE_DIR, 'bot_database.db'))

class UserMessage(Model):
    user_id = IntegerField()
    username = TextField(null=True)
    first_name = TextField(null=True)
    message_text = TextField(null=True)
    message_type = TextField(default='text')
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db