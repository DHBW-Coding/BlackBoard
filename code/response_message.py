from enum import Enum

class ResponseMessage(Enum):
    BB_IS_EMPTY = (200, {"message": "Blackboard is empty."})
    SUCCESS = (200, {"message": "Success"})
    INVALID_PARAMETERS = (400, {"error": "Invalid Parameters provided."})
    BB_NOT_FOUND = (404, {"error": "Blackboard not found."})
    BB_EXISTS_ALREADY = (409, {"error": "Blackboard already exists."})
    INTERNAL_ERROR = (500, {"error": "Internal server error."})

    def __init__(self, http_code, response_body):
        self.http_code = http_code
        self.response_body = response_body
