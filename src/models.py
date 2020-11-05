from database import db
import peewee

class User(peewee.Model):
    token = peewee.CharField(primary_key = True, null = True)
    name = peewee.CharField(null = True)
    email = peewee.CharField(null = True)
    password = peewee.CharField(null = True)

    class Meta:
        database = db

class Secret(peewee.Model):
    title = peewee.CharField(null = True)
    description = peewee.CharField(null = True)
    monetary_value = peewee.IntegerField(null = True)
    date = peewee.DateField(null = True)
    place = peewee.CharField(null = True)
    latitude = peewee.IntegerField(null = True)
    longitude = peewee.IntegerField(null = True)
    token =  peewee.ForeignKeyField(User, backref = 'secrets', to_field = 'token')

    class Meta: 
        database = db