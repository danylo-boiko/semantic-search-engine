from enum import StrEnum


class StreamEvent(StrEnum):
    STREAM_START = "stream-start"
    STREAM_END = "stream-end"
    SEARCH_START = "search-start"
    SEARCH_END = "search-end"
    AGGREGATION_START = "aggregation-start"
    AGGREGATION_END = "aggregation-end"
    MESSAGE_START = "message-start"
    MESSAGE_END = "message-end"
    CONTENT_START = "content-start"
    CONTENT_DELTA = "content-delta"
    CONTENT_END = "content-end"
    CITATION_START = "citation-start"
    CITATION_END = "citation-end"
