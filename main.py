from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from oauth_integration.router import api_router as oauth_router
from db import connect_to_db


app = FastAPI()


@app.on_event("startup")
def startup_func():
    connect_to_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(oauth_router)
app.include()