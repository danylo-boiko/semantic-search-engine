import asyncio

from uuid import uuid4
from typing import AsyncGenerator, Any

from cohere import ClientV2, SystemChatMessageV2, UserChatMessageV2, Document, StreamedChatResponseV2
from api.enums import StreamEvent
from api.models import AggregatedPage
from api.schemas import (
    Page,
    StreamResponse,
    StreamStart,
    StreamEnd,
    SearchStart,
    SearchEnd,
    AggregationStart,
    AggregationEnd,
    MessageStart,
    MessageEnd,
    ContentStart,
    ContentDelta,
    ContentEnd,
    CitationStart,
    CitationEnd
)
from api.services import PageService
from api.settings import Settings


class SearchService:
    def __init__(self) -> None:
        self._settings = Settings()
        self._page_service = PageService()
        self._cohere_client = ClientV2(self._settings.cohere.api_key)

    async def generate_search_stream(self, query: str) -> AsyncGenerator[StreamResponse, Any]:
        # Start the stream
        yield StreamStart(id=uuid4())

        # Start the search process
        yield SearchStart()

        pages = self._page_service.get_pages(query)

        # End the search process
        yield SearchEnd(pages=[Page.from_mongo(page) for page in pages])

        # If no pages are found, end the stream early
        if not pages:
            yield StreamEnd()
            return

        # Start the aggregation process
        yield AggregationStart()

        aggregated_pages = await self._page_service.aggregate_pages(pages)

        # End the aggregation process
        yield AggregationEnd()

        # If no pages are aggregated, end the stream early
        if not aggregated_pages:
            yield StreamEnd()
            return

        # Yield responses from the chat stream
        async for stream_response in self._generate_chat_stream(query, aggregated_pages):
            yield stream_response

        # End the stream
        yield StreamEnd()

    async def _generate_chat_stream(self, query: str, pages: list[AggregatedPage]) -> AsyncGenerator[StreamResponse, Any]:
        chat_steam = self._cohere_client.chat_stream(
            model=self._settings.cohere.model_name,
            messages=[
                SystemChatMessageV2(content=self._settings.cohere.system_prompt),
                UserChatMessageV2(content=query)
            ],
            documents=[Document(id=page.id, data={"content": page.content}) for page in pages],
        )

        for cohere_response in chat_steam:
            yield self._handle_cohere_response(cohere_response)

            await asyncio.sleep(0)

    def _handle_cohere_response(self, response: StreamedChatResponseV2) -> StreamResponse:
        handlers = {
            StreamEvent.MESSAGE_START: lambda _: MessageStart(),
            StreamEvent.MESSAGE_END: lambda _: MessageEnd(),
            StreamEvent.CONTENT_START: lambda x: ContentStart(text=x.delta.message.content.text),
            StreamEvent.CONTENT_DELTA: lambda x: ContentDelta(text=x.delta.message.content.text),
            StreamEvent.CONTENT_END: lambda _: ContentEnd(),
            StreamEvent.CITATION_START: lambda x: CitationStart(
                start=x.delta.message.citations.start,
                end=x.delta.message.citations.end,
                text=x.delta.message.citations.text,
                sources=[source.id for source in x.delta.message.citations.sources]
            ),
            StreamEvent.CITATION_END: lambda _: CitationEnd(),
        }

        if response.type not in handlers:
            raise ValueError(f"Response type {response.type} is not supported")

        return handlers[response.type](response)
