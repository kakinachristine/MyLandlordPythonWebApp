from peewee import *
from os import path
connection = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(connection,"land_lord.db"))
#create the user table
class Users(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

class House(Model):
    houseName = CharField()
    contacts = CharField()
    price = DecimalField()
    description = CharField()
    address = CharField()
    county = CharField()
    subCounty = CharField()
    image = CharField()
    # image2 = CharField()
    # image3 = CharField()
    # image4 = CharField()
    # image5 = CharField()


    class Meta:
        database = db


Users.create_table(fail_silently=True)
House.create_table(fail_silently=True)