from pydantic import BaseModel

from API.models.Enum.OrderEnum import OrderEnum
from API.models.Enum.StatusEnum import StatusEnum
from API.models.Enum.PriorityEnum import PriorityEnum

class FilterRequest(BaseModel):
    status: StatusEnum = StatusEnum.all
    priority: PriorityEnum = PriorityEnum.all
    order: OrderEnum = OrderEnum.date_desc