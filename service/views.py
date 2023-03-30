from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from core import templates
# from core.db import database

router = APIRouter()


@router.get('/')
async def index(request: Request):
    # print(posts.select())
    post_list = [1,2,3]
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'post_list': post_list
        }
    )


