from pydantic import BaseModel

from api.models import Page as PageDocument


class Page(BaseModel):
    id: str
    title: str
    url: str
    similarity_score: float

    @classmethod
    def from_mongo(cls, page: PageDocument) -> "Page":
        return cls(
            id=str(page.id),
            title=page.title,
            url=page.url,
            similarity_score=page.similarity_score
        )
