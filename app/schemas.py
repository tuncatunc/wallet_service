from typing import Optional
from pydantic import BaseModel


class Item (BaseModel):
    id: int
    title: str
    content: str
    public: bool = False
    rating: int = 0
