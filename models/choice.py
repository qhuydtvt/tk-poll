from mongoengine import *
from models.poll import *

class Choice(Document):
    poll = ReferenceField('Poll')
    value = StringField(max_length=60)

    @classmethod
    def with_poll(cls, poll):
        if poll is None:
            return None
        return Choice.objects(poll=poll)
