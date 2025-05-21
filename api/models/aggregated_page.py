from dataclasses import dataclass

from api.models.page import Page


@dataclass
class AggregatedPage:
    id: str
    title: str | None
    url: str
    content: str

    @classmethod
    def from_mongo(cls, page: Page, elements: list[str]) -> "AggregatedPage":
        return cls(
            id=str(page.id),
            title=page.title,
            url=page.url,
            content=" ".join(elements)
        )
