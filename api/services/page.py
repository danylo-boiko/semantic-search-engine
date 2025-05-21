from collections import defaultdict

from langchain_community.document_loaders import UnstructuredURLLoader
from transformers import AutoModel
from unstructured.cleaners.core import clean_extra_whitespace

from api.models import AggregatedPage, Page
from api.repositories import PageRepository
from api.settings import Settings
from api.utils import remove_diacritics, remove_cites, normalize_punctuation


class PageService:
    def __init__(self) -> None:
        self._settings = Settings()
        self._page_repository = PageRepository()
        self._supported_unstructured_categories = {"NarrativeText"}
        self._post_processors = [remove_diacritics, remove_cites, clean_extra_whitespace, normalize_punctuation]
        self._embedding_model = AutoModel.from_pretrained(self._settings.embedding.model_name, trust_remote_code=True)

    def get_pages(self, query: str, top_k: int = 5, min_similarity_score: float = 0.65) -> list[Page]:
        query_embedding = self._embedding_model.encode(query, task="retrieval.query")

        return self._page_repository.get_pages(query_embedding.tolist(), top_k, min_similarity_score)

    async def aggregate_pages(self, pages: list[Page]) -> list[AggregatedPage]:
        page_elements = await self._fetch_page_elements([page.url for page in pages])

        aggregated_pages = []

        for page in pages:
            elements = page_elements.get(page.url, [])

            if not elements:
                continue

            aggregated_pages.append(AggregatedPage.from_mongo(page, elements))

        return aggregated_pages

    async def _fetch_page_elements(self, urls: list[str]) -> dict[str, list[str]]:
        loader = UnstructuredURLLoader(
            urls=urls,
            mode="elements"
        )

        page_elements = defaultdict(list)

        for element in await loader.aload():
            url, category = element.metadata.get("url", None), element.metadata.get("category", None)

            if not url or category not in self._supported_unstructured_categories:
                continue

            for post_processor in self._post_processors:
                element.page_content = post_processor(element.page_content)

            page_elements[url].append(element.page_content)

        return page_elements
