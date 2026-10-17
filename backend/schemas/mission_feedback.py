from typing import Literal
from pydantic import BaseModel

class MissionFeedbackRequest(BaseModel):
    feedback: Literal["helpful", 'not_for_me', 'not_sure']