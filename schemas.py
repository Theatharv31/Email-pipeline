from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import datetime


class EmailIn(BaseModel):
    sender: str
    subject: str
    timestamp: datetime
    links: List[HttpUrl]


class EmailOut(EmailIn):
    id: int

    class Config:
        orm_mode = True
