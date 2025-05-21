from functools import lru_cache

from api.services import SearchService


@lru_cache(maxsize=1)
def get_search_service() -> SearchService:
    return SearchService()


def warm_cache() -> None:
    get_search_service()
