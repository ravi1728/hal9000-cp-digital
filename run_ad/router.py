from fastapi import APIRouter
from fastapi import Query
from fastapi import status
from fastapi.responses import JSONResponse

from run_ad.helpers import run_fb_add_helper


api_router = APIRouter()


@api_router.get("/run-fb-add")
def run_fb_add(lead_form_link: str = Query(...), creative_url: str = Query(...)):
    try:
        run_fb_add_helper(lead_form_link, creative_url)
        return JSONResponse(status_code=status.HTTP_200_OK, content="success")
    except Exception as exc:
        raise exc
