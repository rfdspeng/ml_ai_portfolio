from fastapi import FastAPI
from backend.routers import retrieve, chat
from backend.models.retriever import BookRetriever
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.bookretriever = BookRetriever(credentials, collection_name="best-book-ever", top_k=5)
    yield
    app.state.bookretriever.close()

app = FastAPI(lifespan=lifespan)

# app.include_router(retrieve.router, prefix="/retrieve", tags=["retrieve"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"Welcome Message": "Welcome to the bookstore!"}