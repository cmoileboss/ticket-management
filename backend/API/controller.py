from typing import List

from fastapi import APIRouter

from API.schemas.TicketCountStatus import TicketCountStatus
from API.schemas.Ticket import Ticket

from API.models.TicketCreate import TicketCreate
from API.models.StatusUpdate import StatusUpdate
from API.models.FilterRequest import FilterRequest

from API.service import count_status, filter_tickets, read_json_file, write_json_file, delete_ticket_by_id, update_json_ticket_status

import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/tickets", tags=["tickets"])

# GET endpoints
@router.get("/", response_model=List[Ticket], status_code=200)
async def root():
   result = read_json_file()
   logger.info("Fetched all tickets")
   return result

@router.get("/count-status", response_model=TicketCountStatus, status_code=200)
async def count_status_endpoint():
   result = count_status()
   logger.info("Counted ticket statuses")
   return result

# DELETE endpoints
@router.delete("/{id}", status_code=204)
async def delete_ticket(id: int):
   delete_ticket_by_id(id)
   logger.info(f"Deleted ticket with ID {id}")

# POST endpoints
@router.post("/", response_model=Ticket, status_code=201)
async def create_ticket(ticket: TicketCreate):
   result = write_json_file(ticket)
   logger.info("Created a new ticket")
   return result

@router.post("/filter", response_model=List[Ticket], status_code=200)
def getFilteredOrderedTickets(filter_request: FilterRequest):
   status = filter_request.status.value
   priority = filter_request.priority.value
   order = filter_request.order.value

   filtered_tickets = filter_tickets(status, priority, order)
   return filtered_tickets


# PATCH endpoints
@router.patch("/{id}", response_model=Ticket, status_code=200)
async def update_ticket_status(id: int, status_update: StatusUpdate):
   result = update_json_ticket_status(id, status_update.status)
   logger.info(f"Updated ticket with ID {id} to status {status_update.status}")
   return result
