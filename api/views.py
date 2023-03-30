import json
from typing import List
from fastapi import APIRouter, Depends, Request, Body

from pydantic import BaseModel
from utils.response import json_response, RespCode
from core.config import BOT_DESC, API_KEY, logger

import openai
openai.api_key = API_KEY

router = APIRouter()

@router.post("/chat", summary="chatgpt")
async def openai_chat_request(
        messages: str = Body(..., description="json"),
):
    """
    :param messages:
    :return:
    """
    code = RespCode.SUCCESS
    m = json.loads(messages)

    if m.get("messages")[0].get("role") != 'system':
        m["messages"].insert(0, {
            "role": "system",
            "content": BOT_DESC
        })

    completion = await openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                              messages=m["messages"])
    logger.info(completion.choices[0].message.content)
    data = {"messages": m.get("messages", []), 
            "reply": "AI可以替代一些人类工作，但不是所有工作都可以被替代。"}

    if code != RespCode.SUCCESS:
        return json_response(code, reason=data)

    return json_response(code, data=data)

