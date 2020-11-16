from pydantic import BaseModel
from typing import Optional


class DataNotebook(BaseModel):
    note_id: int
    title: Optional[str]
    text: Optional[str]
    checked: Optional[bool]
