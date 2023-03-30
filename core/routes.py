from fastapi import APIRouter
from service import views
from api import views as api_views

# page
page_routes = APIRouter()
page_routes.include_router(views.router, prefix="")

# api
api_routes = APIRouter()
api_routes.include_router(api_views.router, prefix='/v1')
