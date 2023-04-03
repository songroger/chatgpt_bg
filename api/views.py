import json
from typing import List
from fastapi import APIRouter, Depends, Request, Body

from pydantic import BaseModel
from utils.response import json_response, RespCode
from core.config import BOT_DESC, API_KEY, MODEL, logger
from core import openai

router = APIRouter()

@router.post("/chat", summary="chatgpt")
async def openai_chat_request(
        request: Request,
        # messages: str = Body(..., description="json"),
):
    """
    :param messages:
    :return:
    """
    code = RespCode.SUCCESS
    m = json.loads(await request.body())

    if m.get("messages")[0].get("role") != 'system':
        m["messages"].insert(0, {
            "role": "system",
            "content": BOT_DESC
        })

    completion = await openai.ChatCompletion.acreate(model=MODEL, 
                                              messages=m["messages"])
    # logger.info(completion.choices[0].message.content)
    reply = completion.choices[0].message.content
    if not reply:
        msg = "No reply, try again"
        return json_response(RespCode.FAILURE, msg=msg)

    m.get("messages").append(completion.choices[0].message)
    data = {"messages": m.get("messages", []), 
            "reply": reply}

    return json_response(code, data=data)



@router.post("/mykey", summary="query_key")
async def query_key_request(request: Request):
    m = json.loads(await request.body())

    data={"key": m.get("orderId")}

    return json_response(code, data=data)