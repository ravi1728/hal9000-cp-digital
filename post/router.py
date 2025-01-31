from fastapi import APIRouter
from fastapi import Query
from fastapi import status
from fastapi.responses import JSONResponse

from post.helpers import get_token_and_post


api_router = APIRouter()


@api_router.get("/fb-post")
def fb_post(cp_id: str = Query(...), image_url: str = Query(...)):
    try:
        get_token_and_post(cp_id, image_url)
        return JSONResponse(status_code=status.HTTP_200_OK, content="success")
    except Exception as exc:
        raise exc
