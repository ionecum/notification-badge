# uvicorn_config.py
from uvicorn.config import Config
from myproj.asgi import application

config = Config(app=application, port=8001)
