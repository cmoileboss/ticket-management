from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from API.models.Enum.StatusEnum import StatusEnum
from API.models.Enum.PriorityEnum import PriorityEnum

class TicketCreate(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=10, max_length=500)
    status: StatusEnum 
    tags: list[str]
    priority: PriorityEnum
    createdAt: str = Field(
        description="Date au format YYYY-MM-DD",
        examples=["2026-02-09"],
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d")
    )