from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from oauth_integration.router import api_router as oauth_router
from post.router import api_router as post_router
from run_ad.router import api_router as run_ad_router


app = FastAPI()


@app.on_event("startup")
def startup_func():
    pass

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(oauth_router)
app.include_router(post_router)
app.include_router(run_ad_router)