from typing import Any, Optional
from pydantic.v1 import BaseModel


# OopCompanion:suppressRename


class SuccessResponse(BaseModel):
    """
    成功的响应模型，包含数据。
    """
    code: int = 200
    msg: str = "Success"
    data: Any

class ErrorResponse(BaseModel):
    """
    错误的响应模型，包含错误信息。
    """
    code: int = 400
    msg: str = "Error"
    error: Optional[Any] = None
