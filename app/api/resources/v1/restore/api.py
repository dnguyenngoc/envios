# import
from fastapi import APIRouter, BackgroundTasks
from utils.time import now_utc
import uuid
import json
from init import redis
from api.resources.v1.restore.bg import restore_process

router = APIRouter()


@router.post("/process/{device_id}")
async def restore(device_id: str,
            background_tasks: BackgroundTasks):

    # create request uuid
    start_time = now_utc().timestamp()
    request_id = str(uuid.uuid5(uuid.NAMESPACE_OID, "restore" + str(start_time)))
    
    # run process in backgroud
    background_tasks.add_task(restore_process, request_id, device_id)
    
    return {
        'time_request': start_time,
        'device_id': device_id,
        'request_id': request_id
    }
    

# load result from redis
@router.get('/status/{request_id}')
def status(request_id: str):
    return json.loads(redis.get(request_id))