from pydantic import BaseModel
from models.StatusEnum import StatusEnum
from models.PriorityEnum import PriorityEnum

class FilterRequest(BaseModel):
    status: str = "all"
    priority: str = "all"
    order: str = "date desc"