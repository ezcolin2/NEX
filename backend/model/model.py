from mongoengine import Document, StringField, IntField, ListField
class Character(Document):
    name = StringField()
    appearance = StringField()
    conversations = ListField(StringField(), default=[])