from pydantic import BaseModel, Field


class TicketCountStatus(BaseModel):
    open: int = Field(ge=0)
    in_progress: int = Field(ge=0)
    closed: int = Field(ge=0)