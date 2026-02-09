from pydantic import BaseModel

from API.models.Enum.StatusEnum import StatusEnum


class StatusUpdate(BaseModel):
    status: StatusEnum