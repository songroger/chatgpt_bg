API info:


API definition:


url: /api/v1/chat
method: post
payload: 

```json
{
    "messages": [{
        "role": "user",
        "content": "Ai会替代人类工作吗"
    }]
}
```

response:

```json
{
    "code": 200,
    "errorMsg": "",
    "data": {
        "messages": [
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
            },
            {
                "role": "user",
                "content": "Ai会替代人类工作吗"
            }
        ],
        "reply": "AI可以替代一些人类工作，但不是所有工作都可以被替代。"
    }
}
```


## Config first

### env
Change file `.env.tmpt` to `.env`，and write your own DB url.

```bash 
# 1/ init
alembic init migrations 

# 2/ database config
# alembic.ini 
sqlalchemy.url = mysql://root:Root1024@localhost/fastapi

# migrations/env.py
import sys 
sys.path = ['', '..'] + sys.path[1:]
from service.models import Base

...
target_metadata = Base.metadata  # one app model 
target_metadata = [Base.metadata, Base2.metadata]  # app models

# 3/ alebic init
alembic revision --autogenerate -m "init"

# 4/ alembic upgrade
alembic upgrade head 
```


## start

Python packages are listed in requirements.txt, install them. 
`pip install -r requirements.txt`

1. command：
    `python main.py`

2. docker：
    `docker build -t ai-fastapi:v1.0 .`
    `docker run -p 80:80 -d -e DB_CONNECTION="mysql://root:root@127.0.0.1/fastapi" ai-fastapi:v1.0 ./start.sh `

3. gunicorn：
    `gunicorn -k uvicorn.workers.UvicornWorker --bind "0.0.0.0:8080" --log-level debug main:app`

    `gunicorn -k uvicorn.workers.UvicornWorker -c "gunicorn_conf.py" main:app`


## celery[TODO]

    `celery -A worker.celery_task worker -l debug`
    `celery -A worker.celery_task worker -l info -B`
