from mongoengine import Document
from mongoengine.fields import StringField, BooleanField

class Client(Document):
    fullname = StringField()
    email = StringField()
    sent = BooleanField()
    meta = {"collection": 'clients'}