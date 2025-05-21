from typing import Any

from mongoengine import Document, ObjectIdField, StringField, FloatField


class Page(Document):
    id = ObjectIdField(primary_key=True)
    title = StringField()
    url = StringField(required=True)
    similarity_score = FloatField(required=True)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Page":
        return cls(
            id=data["_id"],
            title=data["title"],
            url=data["url"],
            similarity_score=data["similarity_score"]
        )
