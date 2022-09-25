
# import
from fastapi import APIRouter, BackgroundTasks
from utils.time import now_utc
import json
from init import redis
from api.resources.v1.restore.bg import restore_process
from api.entities.v1.restore import Status
import subprocess


router = APIRouter()


@router.post("/process/{device_id}/{request_id}")
async def restore(device_id: str, 
                  request_id: str,
                  background_tasks: BackgroundTasks):

    # create request uuid
    start_time = now_utc().timestamp()
    
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

    
@router.post('/status/')
def status(data: Status):
    result = []
    for item in data.requests:
        result.append(json.loads(redis.get(item)))
    return result


@router.post('/remove-all-bg/')
def remove_background(
    data: Status,
):
    for request_id in data.requests:
        rst = subprocess.Popen(["ps ax | grep" + " {}".format(request_id)], stdout=subprocess.PIPE)
        stdout = rst.stdout
        result = []
        for line in stdout:
            _str = line.decode('utf-8')
            print(_str)
