from typing import Any
from app.schema.response import SuccessResponse, ErrorResponse


class ResponseTool:

    @classmethod
    def success(cls,data: Any):
        return SuccessResponse(code=200, msg="Success", data=data)

    @classmethod
    def error(cls, error: Any,code:int = 400, msg: str = "Error"):
        return ErrorResponse(msg=msg, error=error)

    @classmethod
    def not_found(cls, error: Any, code:int = 404,  msg: str = "Not Found"):
        return ErrorResponse(code=code, msg=msg, error=error)

    @classmethod
    def unauthorized(cls, error: Any,code:int = 401,  msg: str = "Unauthorized"):
        return ErrorResponse(code=code, msg=msg, error=error)

    @classmethod
    def forbidden(cls, error: Any | None,code:int = 403, msg: str = "Forbidden"):
        return ErrorResponse(code=code, msg=msg, error=error)

    @classmethod
    def gateway_error(cls, error: Any | None, code:int = 502, msg: str = "GatewayError"):
        return ErrorResponse(code=code, msg=msg, error=error)
