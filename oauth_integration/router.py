from fastapi import APIRouter
from fastapi import Query
from fastapi import status
from fastapi.responses import JSONResponse

from oauth_integration.helpers import fb_oauth_helper

api_router = APIRouter()


@api_router.get("/fb-oauth")
def fb_oauth(
        code: str = Query(...),
        state: str = Query(...),
):
    try:
        fb_oauth_helper(code, state)
        return JSONResponse(status_code=status.HTTP_200_OK, content="success")
    except Exception as exc:
        raise exc
