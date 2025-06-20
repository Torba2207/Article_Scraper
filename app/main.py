from fastapi import FastAPI
from .database import engine, Base
from .models import source, article


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Web Scraper API",
    description="API for scraping using Selenium",
    version="0.1.0"
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Scraper API!"}
