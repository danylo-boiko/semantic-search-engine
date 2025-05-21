from hashlib import md5
from urllib.parse import unquote

from langcodes import Language
from scrapy.http import Response
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from unstructured.documents.elements import Element
from unstructured.partition.html import partition_html
from unstructured.cleaners.core import clean_extra_whitespace

from crawler.items import CrawledPage
from crawler.utils import remove_diacritics, remove_cites, normalize_punctuation


class UnstructuredSpider(RedisCrawlSpider):
    name = "unstructured"
    rules = [Rule(LinkExtractor(deny_domains=["archive.org"]), callback="parse", follow=True)]

    def __init__(self) -> None:
        super().__init__()
        self._supported_unstructured_categories = {"NarrativeText"}
        self._post_processors = [remove_diacritics, remove_cites, clean_extra_whitespace, normalize_punctuation]

    def parse(self, response: Response, **kwargs: dict) -> CrawledPage:
        return CrawledPage(
            title=self._extract_title(response),
            url=unquote(response.url),
            language=self._extract_language(response),
            hash=md5(response.body).hexdigest(),
            elements=self._extract_supported_elements(response)
        )

    def _extract_title(self, response: Response) -> str | None:
        title = response.css("title::text").get()

        return title.strip() if title else None

    def _extract_language(self, response: Response) -> Language | None:
        language = response.css("html::attr(lang)").get()

        if not language:
            return None

        parsed_language = Language.get(language, normalize=True)

        return parsed_language.language

    def _extract_supported_elements(self, response: Response) -> list[Element]:
        constituent_elements = partition_html(
            text=response.text,
            headers=response.headers
        )

        supported_elements = []

        for element in constituent_elements:
            if element.category not in self._supported_unstructured_categories:
                continue

            for post_processor in self._post_processors:
                element.text = post_processor(element.text)

            supported_elements.append(element)

        return supported_elements
