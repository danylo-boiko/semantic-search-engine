from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from api.services import SearchService
from api.v1.dependencies import get_search_service


router = APIRouter()


@router.get("")
async def search(query: str, search_service: SearchService = Depends(get_search_service)) -> StreamingResponse:
    return StreamingResponse(
        (event.model_dump_str() async for event in search_service.generate_search_stream(query)),
        media_type="text/event-stream"
    )
