from enum import Enum
from typing import Any

from app.schema.response import ResponseModel


# OopCompanion:suppressRename


class CustomCode(Enum):
    """
    自定义错误码
    """

    CAPTCHA_ERROR = (40001, '验证码错误')

    @property
    def code(self):
        """
        获取错误码
        """
        return self.value[0]

    @property
    def msg(self):
        """
        获取错误码码信息
        """
        return self.value[1]


class Response:
    """
    统一返回方法

    .. tip::

        此类中的返回方法将通过自定义编码器预解析，然后由 fastapi 内部的编码器再次处理并返回，可能存在性能损耗，取决于个人喜好

    E.g. ::

        @router.get('/test')
        def test():
            return await response_base.success(data={'test': 'test'})
    """  # noqa: E501

    def __response(self,code: int, msg: str, data: Any | None = None) -> ResponseModel:
        return ResponseModel(code=code, msg=msg, data=data)

    async def success(self, *, code: int = 200, msg: str = 'Success', data: Any | None = None) -> ResponseModel:
        """
        请求成功返回通用方法

        :param code: 返回状态码
        :param msg: 返回信息
        :param data: 返回数据
        :return:
        """
        return self.__response(code=code, msg=msg, data=data)

    async def fail(self, *, code: int = 400, msg: str = 'Bad Request', data: Any = None) -> ResponseModel:
        return self.__response(code=code, msg=msg, data=data)


response = Response()