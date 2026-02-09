from datetime import datetime
from pydantic import BaseModel, Field

from API.models.Enum.PriorityEnum import PriorityEnum
from API.models.Enum.StatusEnum import StatusEnum


class Ticket(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum
    priority: PriorityEnum
    tags: list[str]
    createdAt: datetime