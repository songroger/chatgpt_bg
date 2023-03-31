import openai
from fastapi.templating import Jinja2Templates
from core import config

templates = Jinja2Templates(directory=config.TEMPLATE_DIR)

openai.api_key = config.API_KEY