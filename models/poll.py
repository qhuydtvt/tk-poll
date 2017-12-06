from mongoengine import *
from shortuuid import ShortUUID
import string

class Poll(Document):
    code = StringField()
    weighted = BooleanField(default=True)
    final_pick_count = IntField()

    @classmethod
    def create(cls):
        alphabet = string.ascii_uppercase
        p = Poll(code=ShortUUID(alphabet=alphabet).random(length=6))
        return p
