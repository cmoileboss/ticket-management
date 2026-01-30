import json
from models import StatusEnum, StatusEnum, TicketCreate


filepath = 'tickets.json'


def read_json_file():
    """
    Reads a JSON file and returns its content as a dictionary.
    Returns:
        dict: {"status": int, "message": str, "data": list}
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return {"status": 200, "message": "Success", "data": data}


def write_json_file(json_object : TicketCreate):
    """
    Writes a dictionary to a JSON file.
    Args:
        json_object (dict): The dictionary to write to the JSON file.
    Returns:
        dict: {"status": int, "message": str, "data": dict}
    """
    read_response = read_json_file()
    data = read_response["data"]
    max_id = get_max_id()
    if max_id is None:
        return 0
    newObject = {"id": max_id + 1, "title": json_object.title, "description": json_object.description,
                 "status": json_object.status.value, "tags": json_object.tags,
                 "priority": json_object.priority.value, "createdAt": json_object.createdAt}
    data.append(newObject)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return {"status": 201, "message": "Objet ajouté avec succès.", "data": newObject}

def count_status():
    """
    Counts the occurrences of each status in the JSON file.
    Returns:
        dict: {"status": int, "message": str, "data": dict}
    """
    read_response = read_json_file()
    data = read_response["data"]
    if len(data) == 0:
        return {"status": 404, "message": "Counting impossible", "details": "No tickets in database"}
    status_count = {}
    for item in data:
        status = item.get("status")
        if status:
            if status in status_count:
                status_count[status] += 1
            else:
                status_count[status] = 1
    return {"status": 200, "message": "Status counted with success", "data": status_count}


def delete_ticket_by_id(ticket_id: int):
    """
    Deletes a ticket from the JSON file by its ID.
    Args:
        ticket_id (int): The ID of the ticket to delete.
    Returns:
        dict: {"status": int, "message": str, "data": None}
    """
    read_response = read_json_file()
    data = read_response["data"]
    if len(data) == 0:
        return {"status": 404, "message": "Deletion failed", "details": "No tickets in database"}
    new_data = [item for item in data if item.get("id") != ticket_id]
    if len(new_data) == len(data):
        return {"status": 404, "message": "Deletion failed", "details": f"Ticket of id: {ticket_id} not found"}
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4, ensure_ascii=False)
    return {"status": 200, "message": f"Ticket of id: {ticket_id} has been deleted.", "data": None}


def update_json_ticket_status(ticket_id: int, new_status: StatusEnum):
    """
    Updates the status of a ticket in the JSON file by its ID.
    Args:
        ticket_id (int): The ID of the ticket to update.
        new_status (str): The new status to set.
    Returns:
        dict: {"status": int, "message": str, "data": dict}
    """
    read_response = read_json_file()
    data = read_response["data"]
    if len(data) == 0:
        return {"status": 404, "message": "Update failed", "details": "No tickets in database"}
    ticket_found = False
    updated_item = None
    for item in data:
        if item.get("id") == ticket_id:
            item["status"] = new_status.value
            ticket_found = True
            updated_item = item
            break
    if not ticket_found:
        return {"status": 404, "message": "Update failed", "details": f"Ticket of id: {ticket_id} not found."}
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return {"status": 200, "message": f"The status of ticket of id: {ticket_id} has been updated.", "data": updated_item}


def get_max_id():
    """
    Retrieves the maximum ID from the tickets in the JSON file.
    Returns:
        dict: {"status": int, "message": str, "data": int}
    """
    read_response = read_json_file()
    data = read_response["data"]
    if len(data) == 0:
        return None
    max_id = max(item.get("id", 0) for item in data)
    return max_id
