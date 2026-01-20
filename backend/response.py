from ast import Dict
from ctypes import Union
from typing import Any


class Response:
    status: int
    message: str
    data: Dict[str, Any]

    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data