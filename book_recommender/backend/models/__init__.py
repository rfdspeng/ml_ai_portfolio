from .assistant import BookAssistant
from .retriever import BookRetriever
from pydantic import BaseModel

class UserQuery(BaseModel):
    userid: str
    message: str

# Define the public API of this module
__all__ = ["BookAssistant", "BookRetriever", "UserQuery"]