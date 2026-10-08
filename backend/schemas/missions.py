from pydantic import BaseModel

class MissionResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    difficulty: str
    social_required: bool
    energy_required: str