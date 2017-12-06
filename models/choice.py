from mongoengine import *
from models.poll import *

class Choice(Document):
    poll = ReferenceField('Poll')
    value = StringField(max_length=30)
