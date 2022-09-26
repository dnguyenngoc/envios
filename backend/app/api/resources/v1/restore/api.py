
# import
from fastapi import APIRouter, BackgroundTasks, HTTPException
from utils.time import now_utc
import json
from init import redis
from api.resources.v1.restore.bg import restore_process
from api.entities.v1.restore import Status
import sh
import signal
import os


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
        data = redis.get(item)
        if data != None:
            result.append(json.loads(data))
    return result


def kill_process(pid):
    os.killpg(os.getpgid(pid), signal.SIGTERM)  


@router.post('/remove-all-bg/')
def remove_background(filter: str = 'idevicerestore'):
    print('[REMOVE-BG]')
    checks = {
        'idevicerestore': True
    }
    try:
        if checks[filter] == False:
            raise HTTPException(status_code=400, detail='filter not support!')
    except:
        raise HTTPException(status_code=400, detail='filter not support!')
    try:  
        data = sh.grep(sh.ps("ax"), filter)
        for item in data:
            print('  - kill:', item)
            pid =int(item.split(' ')[0])
            kill_process(pid)
        return {"detail": data}
    except Exception as e:
        print(e)
        return {"detail": 'all process have been closed!'}