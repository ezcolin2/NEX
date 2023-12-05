from mongoengine import Document, StringField, IntField, ListField, ReferenceField
class Novel(Document):
    name = StringField()
    summary = StringField()
    url = StringField()
    uuid = StringField()
class NovelCharacter(Document):
    name = StringField()
    appearance = StringField()
    conversations = ListField(StringField(), default=[])
    novel = ReferenceField(Novel, reverse_delete_rule=2)