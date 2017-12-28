from mongoengine import *
from shortuuid import ShortUUID
import string

class Poll(Document):
    code = StringField()
    weighted = BooleanField(default=True)
    final_pick = IntField()

    @classmethod
    def create(cls, final_pick):
        alphabet = string.ascii_uppercase
        code = ShortUUID(alphabet=alphabet).random(length=6)
        p = Poll(code=code, final_pick=final_pick)
        return p

    @classmethod
    def with_code(cls, code):
        if code is None:
            return None
        return Poll.objects(code=code).first()
