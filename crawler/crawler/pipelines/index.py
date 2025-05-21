import datetime

from mongoengine import connect, disconnect
from scrapy import Spider
from scrapy.utils.log import logger
from transformers import AutoModel

from crawler.items import CrawledPage
from crawler.models import Page
from crawler.settings import Settings
from crawler.summarizers import MultilingualTextRankSummarizer


class IndexPipeline:
    def __init__(self) -> None:
        self._settings = Settings()
        self._summarizer = MultilingualTextRankSummarizer()
        self._embedding_model = AutoModel.from_pretrained(self._settings.embedding.model_name, trust_remote_code=True)
        self._max_words_count = int(
            self._embedding_model.config.max_position_embeddings * self._settings.embedding.token_to_word_ratio
        )

    def open_spider(self, _: Spider) -> None:
        connect(self._settings.mongo.db_name, host=self._settings.mongo.url)

    def close_spider(self, _: Spider) -> None:
        disconnect()

    def process_item(self, crawled_page: CrawledPage, _: Spider) -> CrawledPage:
        if not crawled_page.elements or crawled_page.language not in self._settings.embedding.supported_languages:
            return crawled_page

        meaningful_sentences = self._summarizer(crawled_page.content, crawled_page.language, self._max_words_count)

        page_embedding = self._embedding_model.encode(". ".join(meaningful_sentences), task="retrieval.passage")

        page = Page(
            title=crawled_page.title,
            url=crawled_page.url,
            language=crawled_page.language,
            hash=crawled_page.hash,
            embedding=page_embedding.tolist(),
            created_at=datetime.datetime.now(datetime.UTC)
        ).save()

        logger.info(
            f"[Indexed Page] Id: '{page.id}', Title: '{page.title}', Url: '{page.url}', Language: '{page.language}'"
        )

        return crawled_page
