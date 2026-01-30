from datetime import datetime
from pydantic import BaseModel, field_validator
from models.StatusEnum import StatusEnum
from models.PriorityEnum import PriorityEnum

class TicketCreate(BaseModel):
   title: str
   description: str
   status: StatusEnum 
   tags: list[str]
   priority: PriorityEnum
   createdAt: str

   @field_validator('title')
   @classmethod
   def title_must_not_be_empty(cls, v):
       if not v or not v.strip():
           raise ValueError('Title must not be empty')
       return v

   @field_validator('description')
   @classmethod
   def description_must_not_be_empty(cls, v):
       if not v or not v.strip():
           raise ValueError('Description must not be empty')
       return v
   @field_validator('createdAt')
   @classmethod
   def createdAt_must_not_be_empty(cls, v):
       if not v or not v.strip():
           raise ValueError('createdAt must not be empty')
       try:
            datetime.strptime(v, "%Y-%m-%d")
       except ValueError:
            raise ValueError("format de la date incorrect, il doit être YYYY-MM-DD")
       return v
   
