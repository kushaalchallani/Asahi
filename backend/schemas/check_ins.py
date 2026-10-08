from pydantic import BaseModel

class CheckInCreate(BaseModel):
    feeling: str
    note: str | None = None