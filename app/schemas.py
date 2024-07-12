# app/schemas.py
from pydantic import BaseModel

class URLRequest(BaseModel):
    url: str
    expiration: int = None

class URLResponse(BaseModel):
    short_url: str

class URLStats(BaseModel):
    view_count: int
