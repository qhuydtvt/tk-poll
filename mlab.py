import mongoengine


host = "ds033196.mlab.com"
port = 33196
db_name = "tk-poll"
user_name = "admin"
password = "admin"

def mlab_connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())
