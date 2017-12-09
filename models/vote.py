from mongoengine import *
from models.choice import *
from models.poll import *
from shortuuid import ShortUUID


class VotePoint(EmbeddedDocument):
    choice = ReferenceField("Choice")
    point = IntField()


    @classmethod
    def create(cls, choice_id, point):
        return VotePoint(
                choice=Choice.objects().with_id(choice_id),
                point=point)


class Vote(Document):
    poll = ReferenceField('Poll')
    vote_points = EmbeddedDocumentListField("VotePoint")
    voter_name = StringField(max_length=40)
    voter_code = StringField(max_length=6)

    @classmethod
    def create(cls, poll, vote_points, voter_name):
        import string
        alphabet = string.ascii_uppercase
        voter_code = ShortUUID(alphabet=alphabet).random(length=6)
        return Vote(poll=poll, vote_points=vote_points, voter_name=voter_name, voter_code=voter_code)
