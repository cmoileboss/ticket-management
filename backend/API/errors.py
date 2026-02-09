from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError

import json
import logging


logger = logging.getLogger(__name__)


async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):
   logging.error(f"Validation error on {request.url}: {exc.errors()}")
   response = JSONResponse(
      status_code=422,
      content={
         "message": getattr(exc, "detail", "Validation error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )
   return response

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
   logging.error(f"Validation error on {request.url}: {exc.errors()}")
   response = JSONResponse(
      status_code=422,
      content={
         "message": getattr(exc, "detail", "Validation error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )
   return response

async def http_exception_handler(request: Request, exc: HTTPException):
   logging.error(f"HTTP exception on {request.url}: {exc.status_code} - {exc.detail}")
   return JSONResponse(
      status_code=exc.status_code,
      content={
         "message": getattr(exc, "detail", "HTTP error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

async def file_not_found_exception_handler(request: Request, exc: FileNotFoundError):
   logging.error(f"File not found on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=404,
      content={
         "message": getattr(exc, "detail", "File not found"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

async def json_decode_exception_handler(request: Request, exc: json.JSONDecodeError):
   logging.error(f"JSON decode error on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=400,
      content={
         "message": getattr(exc, "detail", "JSON decode error"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

async def permission_exception_handler(request: Request, exc: PermissionError):
   logging.error(f"Permission error on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=403,
      content={
         "message": getattr(exc, "detail", "Permission denied"),
         "details": exc.errors() if hasattr(exc, "errors") else None
      }
   )

async def type_error_handler(request: Request, exc: TypeError):
   logging.error(f"Type error on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=400,
      content={
         "message": getattr(exc, "detail", "Type error"),
         "details": exc.errors() if hasattr(exc, "errors") else str(exc)
      }
   )

async def value_error_handler(request: Request, exc: ValueError):
   logging.error(f"Value error on {request.url}: {str(exc)}")
   return JSONResponse(
      status_code=400,
      content={
         "message": getattr(exc, "detail", "Value error"),
         "details": exc.errors() if hasattr(exc, "errors") else str(exc)
      }
   )