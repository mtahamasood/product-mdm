# main.py
from fastapi import FastAPI
from model import init_db
from router import router

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(router)
