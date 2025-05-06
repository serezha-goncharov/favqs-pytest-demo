from typing import List, Optional
from pydantic import HttpUrl, Field

from api.models import BaseSchema


class UserDetails(BaseSchema):
    favorite: bool
    upvote: bool
    downvote: bool
    hidden: bool


class Quote(BaseSchema):
    id: int
    source: Optional[str] = None
    context: Optional[str] = None
    dialogue: bool
    private: bool
    tags: List[str] = Field(default_factory=list)
    url: HttpUrl
    favorites_count: int = Field(ge=0)
    upvotes_count: int = Field(ge=0)
    downvotes_count: int = Field(ge=0)
    author: str
    author_permalink: str
    body: str
    user_details: UserDetails


class Quotes(BaseSchema):
    page: int = Field(ge=1)
    last_page: bool
    quotes: List[Quote]
