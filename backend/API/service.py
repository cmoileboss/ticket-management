import json
import logging

from fastapi import HTTPException

from API.models.Enum.StatusEnum import StatusEnum
from API.models.TicketCreate import TicketCreate

logger = logging.getLogger(__name__)

filepath = 'tickets.json'


def read_json_file():
    """
    Reads a JSON file and returns its content as a dictionary.
    Returns:
        dict: {"status": int, "message": str, "data": list}
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    logger.debug(f"Successfully read {len(data)} tickets from {filepath}")
    return data
    


def write_json_file(json_object : TicketCreate):
    """
    Writes a ticket to the JSON file.
    Args:
        json_object (TicketCreate): The ticket data to add.
    Returns:
        dict: The newly created ticket
    """
    data = read_json_file()
    max_id = get_max_id()
    if max_id is None:
        logger.warning("No existing tickets, starting with ID 0")
        max_id = 0
    newObject = {
        "id": max_id + 1,
        "title": json_object.title,
        "description": json_object.description,
        "status": json_object.status.value,
        "tags": json_object.tags,
        "priority": json_object.priority.value,
        "createdAt": json_object.createdAt
    }
    data.append(newObject)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    logger.info(f"Created new ticket with ID {newObject['id']}")
    return newObject

def count_status():
    """
    Counts the occurrences of each status in the JSON file.
    Returns:
        dict: {"status": int, "message": str, "data": dict}
    """
    data = read_json_file()
        
    status_count = {
        "Open": 0,
        "In progress": 0,
        "Closed": 0
    }

    if len(data) == 0:
        logger.warning("No tickets in database to count")
        return status_count
    
    for item in data:
        status = item.get("status")
        if status in status_count:
            status_count[status] += 1
    
    normalized_count = {
        "open": status_count["Open"],
        "in_progress": status_count["In progress"],
        "closed": status_count["Closed"]
    }
    
    return normalized_count

def delete_ticket_by_id(ticket_id: int):
    """
    Deletes a ticket from the JSON file by its ID.
    Args:
        ticket_id (int): The ID of the ticket to delete.
    Raises:
        HTTPException: 404 if ticket not found
    """
    data = read_json_file()
    if len(data) == 0:
        logger.warning(f"Cannot delete ticket {ticket_id}: No tickets in database")
        raise HTTPException(status_code=404, detail="No tickets in database")
    new_data = [item for item in data if item.get("id") != ticket_id]
    if len(new_data) == len(data):
        logger.warning(f"Ticket with ID {ticket_id} not found for deletion")
        raise HTTPException(status_code=404, detail=f"Ticket with ID {ticket_id} not found")
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4, ensure_ascii=False)
    logger.info(f"Deleted ticket with ID {ticket_id}")


def update_json_ticket_status(ticket_id: int, new_status: StatusEnum):
    """
    Updates the status of a ticket in the JSON file by its ID.
    Args:
        ticket_id (int): The ID of the ticket to update.
        new_status (StatusEnum): The new status to set.
    Returns:
        dict: The updated ticket
    Raises:
        HTTPException: 404 if ticket not found
    """
    data = read_json_file()
    if len(data) == 0:
        logger.warning(f"Cannot update ticket {ticket_id}: No tickets in database")
        raise HTTPException(status_code=404, detail="No tickets in database")
    ticket_found = False
    updated_item = None
    for item in data:
        if item.get("id") == ticket_id:
            item["status"] = new_status.value
            ticket_found = True
            updated_item = item
            break
    if not ticket_found:
        logger.warning(f"Ticket with ID {ticket_id} not found for update")
        raise HTTPException(status_code=404, detail=f"Ticket with ID {ticket_id} not found")
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    logger.info(f"Updated ticket with ID {ticket_id} to status {new_status.value}")
    return updated_item

def get_max_id():
    """
    Retrieves the maximum ID from the tickets in the JSON file.
    Returns:
        int: The maximum ID found, or None if no tickets exist.
    """
    data = read_json_file()
    if len(data) == 0:
        return None
    max_id = max(item.get("id", 0) for item in data)
    return max_id

def filter_tickets(status: str, priority: str, order: str):
    data = read_json_file()
    filtered_tickets = data.copy()

    if status == "all" and priority != "all":
        filtered_tickets = [item for item in data if item.get("priority") == priority]
        logger.info(f"Fetched tickets with priority {priority}")

    elif priority == "all" and status != "all":
        logger.info(f"Fetched tickets with status {status}")
        filtered_tickets = [item for item in data if item.get("status").lower() == status.lower()]

    elif priority != "all" and status != "all":
        filtered_tickets = [item for item in data if item.get("status").lower() == status.lower() and item.get("priority") == priority]
        logger.info(f"Fetched tickets with status {status} and priority {priority}")

    if (order == 'date desc'):
        logger.info(f"Sorting tickets by date")
        filtered_tickets.sort(key=lambda x: x['createdAt'], reverse=True)

    elif (order == 'date asc'):
        logger.info(f"Sorting tickets by date")
        filtered_tickets.sort(key=lambda x: x['createdAt'], reverse=False)

    elif (order == 'priority'):
        logger.info(f"Sorting tickets by priority")
        priority_order = {'Low': 3, 'Medium': 2, 'High': 1}
        filtered_tickets.sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=False)

    elif (order == 'status'):
        logger.info(f"Sorting tickets by status")
        status_order = {'Open': 2, 'In progress': 1, 'Closed': 3}
        filtered_tickets.sort(key=lambda x: status_order.get(x['status'], 0), reverse=False)

    elif (order == 'alphabetical'):
        logger.info(f"Sorting tickets by alphabetical order")   
        filtered_tickets.sort(key=lambda x: x['title'].lower(), reverse=False)

    return filtered_tickets