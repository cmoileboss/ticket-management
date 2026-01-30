from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from script import count_status, read_json_file, write_json_file, delete_ticket_by_id, update_json_ticket_status
from models.TicketCreate import TicketCreate
from models.StatusUpdate import StatusUpdate

import json
import logging

logging.basicConfig(
    filename="logs.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG
)

# Also log uvicorn messages
uvicorn_logger = logging.getLogger('uvicorn')
uvicorn_logger.setLevel(logging.DEBUG)


app = FastAPI()

logging.info("FastAPI application started")

@app.on_event("shutdown")
def shutdown_event():
    logging.info("FastAPI application shutting down")


origins= [
   "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
   logging.error(f"Validation error on {request.url}: {exc.errors()}")
   response = JSONResponse(
      status_code=422,
      content={
         "status": 422,
         "message": getattr(exc, "detail", "Validation error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )
   return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
   logging.error(f"HTTP exception on {request.url}: {exc.status_code} - {exc.detail}")
   return JSONResponse(
      status_code=exc.status_code,
      content={
         "status": exc.status_code,
         "message": getattr(exc, "detail", "HTTP error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

@app.exception_handler(FileNotFoundError)
async def file_not_found_exception_handler(request: Request, exc: FileNotFoundError):
   logging.error(f"File not found on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=404,
      content={
         "status": 404,
         "message": getattr(exc, "detail", "File not found"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

@app.exception_handler(json.JSONDecodeError)
async def json_decode_exception_handler(request: Request, exc: json.JSONDecodeError):
   logging.error(f"JSON decode error on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=400,
      content={
         "status": 400,
         "message": getattr(exc, "detail", "JSON decode error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

@app.exception_handler(PermissionError)
async def permission_exception_handler(request: Request, exc: PermissionError):
   logging.error(f"Permission error on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=403,
      content={
         "status": 403,
         "message": getattr(exc, "detail", "Permission denied"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

@app.exception_handler(TypeError)
async def type_error_handler(request: Request, exc: TypeError):
   logging.error(f"Type error on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=400,
      content={
         "status": 400,
         "message": getattr(exc, "detail", "Type error"),
         "details": exc.errors() if hasattr(exc, "errors") else str(exc)
      }
   )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
   logging.error(f"Value error on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=400,
      content={
         "status": 400,
         "message": getattr(exc, "detail", "Value error"),
         "details": exc.errors() if hasattr(exc, "errors") else str(exc)
      }
   )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
   logging.error(f"Unexpected error on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=500,
      content={
         "status": 500,
         "message": getattr(exc, "detail", "Internal server error"),
         "details": exc.errors() if hasattr(exc, "errors") else str(exc)
      }
   )



# GET endpoints
@app.get("/tickets")
async def root():
   result = read_json_file()
   logging.info("Fetched all tickets")
   return JSONResponse(status_code=result["status"], content=result)

@app.get("/tickets/count-status")
async def count_status_endpoint():
   result = count_status()
   logging.info("Counted ticket statuses")
   return JSONResponse(status_code=result["status"], content=result)

@app.get("/tickets/status/{status}")
def getByStatus(status: str):
   if (status not in ["open", "in_progress", "closed"]):
      return JSONResponse(
         status_code=400,
         content={
            "status": 400,
            "message": f"Invalid status: {status}. Must be one of ['open', 'in_progress', 'closed'].",
            "data": None
         }
      )
   read_response = read_json_file()
   data = read_response["data"]
   filtered_tickets = [item for item in data if item.get("status") == status]
   return {"status": 200, "message": f"Tickets with status {status} fetched successfully.", "data": filtered_tickets}

@app.get("/tickets/priority/{priority}")
def getByPriority(priority: str):
   if (priority not in ["Low", "Medium", "High"]):
      return JSONResponse(
         status_code=400,
         content={
            "status": 400,
            "message": f"Invalid priority: {priority}. Must be one of ['Low', 'Medium', 'High'].",
            "data": None
         }
      )
   read_response = read_json_file()
   data = read_response["data"]
   filtered_tickets = [item for item in data if item.get("priority") == priority]
   return {"status": 200, "message": f"Tickets with priority {priority} fetched successfully.", "data": filtered_tickets}

# DELETE endpoints
@app.delete("/tickets/{id}")
async def delete_ticket(id: int):
   result = delete_ticket_by_id(id)
   logging.info(f"Deleted ticket with ID {id}")
   return JSONResponse(status_code=result["status"], content=result)

# POST endpoints
@app.post("/tickets")
async def create_ticket(ticket: TicketCreate):
   result = write_json_file(ticket)
   logging.info("Created a new ticket")
   return JSONResponse(status_code=result["status"], content=result)

# PATCH endpoints
@app.patch("/tickets/{id}")
async def update_ticket_status(id: int, status_update: StatusUpdate):
   result = update_json_ticket_status(id, status_update.status)
   logging.info(f"Updated ticket with ID {id} to status {status_update.status}")
   return JSONResponse(status_code=result["status"], content=result)
