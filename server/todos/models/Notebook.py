from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class DataNotebook(BaseModel):
    note_id: int
    title: Optional[str]
    text: Optional[str]
    checked: Optional[bool]
