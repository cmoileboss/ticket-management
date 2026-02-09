import json
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi import HTTPException

from API.controller import router
from API.errors import (
    response_validation_exception_handler,
    request_validation_exception_handler,
    http_exception_handler,
    file_not_found_exception_handler,
    json_decode_exception_handler,
    permission_exception_handler,
    type_error_handler,
    value_error_handler
)


# Configuration du logger
logging.basicConfig(
    filename="logs.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG
)

# Configuration du logger pour la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)

# Configuration du logger pour uvicorn
uvicorn_logger = logging.getLogger('uvicorn')
uvicorn_logger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

def create_app():

    app = FastAPI(title="Ticket Management API", version="1.0.0")
    
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

    app.add_exception_handler(ResponseValidationError, response_validation_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(FileNotFoundError, file_not_found_exception_handler)
    app.add_exception_handler(json.JSONDecodeError, json_decode_exception_handler)
    app.add_exception_handler(PermissionError, permission_exception_handler)
    app.add_exception_handler(TypeError, type_error_handler)
    app.add_exception_handler(ValueError, value_error_handler)

    app.include_router(router)
    
    logging.info("FastAPI application started")
    
    return app

app = create_app()