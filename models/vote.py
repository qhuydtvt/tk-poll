from mongoengine import *
from models.choice import *

class Vote(Document):
    choice = ReferenceField("Choice")
    voter_name = StringField(max_length=40)
