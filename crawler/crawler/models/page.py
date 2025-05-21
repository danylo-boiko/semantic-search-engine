from mongoengine import Document, StringField, ListField, DateTimeField


class Page(Document):
    title = StringField()
    url = StringField(required=True)
    language = StringField(required=True)
    hash = StringField(required=True)
    embedding = ListField(required=True)
    created_at = DateTimeField(required=True)
