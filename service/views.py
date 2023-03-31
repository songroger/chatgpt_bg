from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from core import templates
# from core.db import database

router = APIRouter()


@router.get('/')
async def index(request: Request):

    return templates.TemplateResponse(
        'index.html',
        {
            'request': request
        }
    )
