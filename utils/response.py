import json

from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union
# from utils import constant


class RespCode(object):
    """响应状态码
    """
    SUCCESS = 200
    FAILURE = 40000
    OTHER_ERR = 40001
    INTERNAL_ERR = 40002


def json_response(code: int, data: Union[list, dict] = None, msg: str = '', reason: str = '') -> Response:
    """请求响应
        code (int): [description]
        data (Union[list, dict], optional): 响应数据 Defaults to list().
        msg (str, optional): 响应状态描述 Defaults to ''.
        reason (str, optional): 错误堆栈 Defaults to ''.
    """
    code = int(code) if isinstance(code, str) else code
    data = data if data else list()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': code,
            'errorMsg': msg,
            # 'reason': reason,
            'data': data,
        }
    )
