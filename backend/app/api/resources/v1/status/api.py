
# import
import json
from init import redis
from fastapi import APIRouter
from api.entities.v1.restore import Status


router = APIRouter()


@router.post('/')
def status(data: Status):
    result = []
    for item in data.requests:
        data = redis.get(item)
        if data != None:
            result.append(json.loads(data))
    return result