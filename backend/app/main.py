import os
import logging
from settings import config
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from logging.handlers import TimedRotatingFileHandler
from api.routers import v1
import init

# Fix middleware error in fastapi
middleware =[
    Middleware(CORSMiddleware,
    allow_origins=config.CORS_MIDDLEWARE,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    )
]

# Step up fastapi with openapi_url/middleware
app = FastAPI(title=config.PROJECT_NAME, 
              middleware=middleware,
              openapi_url="/api/openapi.json", 
              docs_url="/api/docs", 
              redoc_url="/api/redoc")

# Handle Logs API
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s")

log_dir = '../logs/'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    
handler = TimedRotatingFileHandler(
    '../logs/{}-{}-{}_{}h-00p-00.log'.format(
        config.u.year, config.u.month, 
        config.u.day , config.u.hour
    ),
    when="midnight", interval=1, encoding='utf8')

handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# Add router v1
app.include_router(v1.router, prefix="/api/v1")
