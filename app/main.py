from fastapi import FastAPI
from .database import engine, Base
from . import models
from .api import sources as sources_api
from .api import articles as articles_api
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Scraper API",
    description="API for managing and scraping articles from various sources.",
    version="1.0.0",
)

app.include_router(sources_api.router)
app.include_router(articles_api.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Scraper API!"}
