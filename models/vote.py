from mongoengine import *
from models.choice import *


class VotePoint(EmbeddedDocument):
    choice = ReferenceField("Choice")
    point = IntField()

    @classmethod
    def create(cls, choice_id, point):
        return VotePoint(
                choice=Choice.objects().with_id(choice_id),
                point=point)


class Vote(Document):
    vote_points = EmbeddedDocumentListField("VotePoint")
    voter_name = StringField(max_length=40)
