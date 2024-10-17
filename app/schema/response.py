from typing import Any

from pydantic.v1 import BaseModel


# OopCompanion:suppressRename


class ResponseModel(BaseModel):
    """
    统一返回模型

    .. tip::

        如果你不想使用 ResponseBase 中的自定义编码器，可以使用此模型，返回数据将通过 fastapi 内部的编码器直接自动解析并返回

    E.g. ::

        @router.get('/test', response_model=ResponseModel)
        def test():
            return ResponseModel(data={'test': 'test'})


        @router.get('/test')
        def test() -> ResponseModel:
            return ResponseModel(data={'test': 'test'})
    """  # noqa: E501

    # model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: int = 200
    msg: str = 'Success'
    data: Any | None = None

