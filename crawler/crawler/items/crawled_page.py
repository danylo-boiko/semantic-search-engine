from dataclasses import dataclass

from unstructured.documents.elements import Element


@dataclass
class CrawledPage:
    title: str | None
    url: str
    language: str | None
    hash: str
    elements: list[Element]

    @property
    def content(self):
        return " ".join(map(str, self.elements))
