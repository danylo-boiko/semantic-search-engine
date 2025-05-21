from abc import ABC
from uuid import UUID, uuid4

from pydantic import BaseModel

from api.enums import StreamEvent
from api.schemas import Page


class StreamResponse(ABC, BaseModel):
    type: StreamEvent = ...

    def model_dump_str(self):
        return f"data: {self.model_dump_json()}\n\n"


class StreamStart(StreamResponse):
    type: StreamEvent = StreamEvent.STREAM_START
    id: UUID


class StreamEnd(StreamResponse):
    type: StreamEvent = StreamEvent.STREAM_END


class SearchStart(StreamResponse):
    type: StreamEvent = StreamEvent.SEARCH_START


class SearchEnd(StreamResponse):
    type: StreamEvent = StreamEvent.SEARCH_END
    pages: list[Page]


class AggregationStart(StreamResponse):
    type: StreamEvent = StreamEvent.AGGREGATION_START


class AggregationEnd(StreamResponse):
    type: StreamEvent = StreamEvent.AGGREGATION_END


class MessageStart(StreamResponse):
    type: StreamEvent = StreamEvent.MESSAGE_START


class MessageEnd(StreamResponse):
    type: StreamEvent = StreamEvent.MESSAGE_END


class ContentStart(StreamResponse):
    type: StreamEvent = StreamEvent.CONTENT_START
    text: str


class ContentDelta(StreamResponse):
    type: StreamEvent = StreamEvent.CONTENT_DELTA
    text: str


class ContentEnd(StreamResponse):
    type: StreamEvent = StreamEvent.CONTENT_END


class CitationStart(StreamResponse):
    type: StreamEvent = StreamEvent.CITATION_START
    start: int
    end: int
    text: str
    sources: list[str]


class CitationEnd(StreamResponse):
    type: StreamEvent = StreamEvent.CITATION_END
