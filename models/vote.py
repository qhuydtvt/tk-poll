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
    def create(cls, poll, vote_points, voter_name, voter_code):
        import string
        alphabet = string.ascii_uppercase
        if voter_code is None:
            voter_code = ShortUUID(alphabet=alphabet).random(length=6)
        return Vote(poll=poll, vote_points=vote_points, voter_name=voter_name, voter_code=voter_code)

    def sum_points(self, choice):
        return sum([vote_point.point for vote_point in self.vote_points if vote_point.choice.id == choice.id])
    
    # @classmethod
    # def find_by_voter_code(cls, voter_code):
    #     if voter_code == None:
    #         return None
    #     else:
    #         return Vote.objects(voter_code=voter_code).first()

    @classmethod
    def find(cls, poll, voter_code):
        return Vote.objects(poll=poll, voter_code=voter_code).first()


    @classmethod
    def with_poll(clas, poll):
        if poll is None:
            return None
        return Vote.objects(poll=poll)
