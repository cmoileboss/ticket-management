from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError

import json
import logging


logger = logging.getLogger(__name__)


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