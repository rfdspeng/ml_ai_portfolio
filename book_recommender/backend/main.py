from fastapi import FastAPI
from backend.routers import chat
from backend.models import BookRetriever
from contextlib import asynccontextmanager
from dotenv import dotenv_values

# Context manager for the FastAPI application
# Instantiate one BookRetriever object to be shared among users and store it in app.state
@asynccontextmanager
async def lifespan(app: FastAPI):
    credentials = dict(dotenv_values(".env"))
    app.state.bookretriever = BookRetriever(credentials, collection_name="best-book-ever", top_k=5)
    yield
    await app.state.bookretriever.close()

app = FastAPI(lifespan=lifespan)

app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"Welcome Message": "Welcome to the bookstore!"}