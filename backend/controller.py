from fastapi import FastAPI
from script import count_status, read_json_file, write_json_file, delete_ticket_by_id, update_json_ticket_status


app = FastAPI()

# GET endpoints
@app.get("/tickets")
async def root():
   return read_json_file()

@app.get("/tickets/count-status")
async def count_status_endpoint():
    return count_status()

# DELETE endpoints
@app.delete("/tickets/{id}")
async def delete_ticket(id: int):
   return delete_ticket_by_id(id)

# POST endpoints
@app.post("/tickets")
async def create_ticket(ticket: dict):
    return write_json_file(ticket)

# PATCH endpoints
@app.patch("/tickets/{id}")
async def update_ticket_status(id: int, status: dict):
   print(status)
   return update_json_ticket_status(id, status['status'])
