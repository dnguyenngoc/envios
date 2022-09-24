import json
from utils.time import now_utc
from init import redis
import json
import time


def restore_process(request_id: str, device_id: str):
    print('{} - [Restore] r: {}, d: {}'.format(now_utc(), request_id, device_id))
    data = {
            'request_id': request_id,
            'device_id': device_id,
            'times':{
                'start_dowload_os': now_utc().timestamp(),
                'end_dowload_os': now_utc().timestamp(),
                'start_verify_os': now_utc().timestamp(),
                'end_verify_os': now_utc().timestamp(),
                'start_restore_os': now_utc().timestamp(),
                'end_restore_os': now_utc().timestamp(),
            },
            'status':{
                'general': 'pending',
                'dowload_os': 'pending',
                'verify_os': None,
                'restore': None
            },
            'logs': ["start dowloading os ...."],
            'error': None
        }
    for i in range(4):
        if i == 0:
            redis.set(request_id, json.dumps(data))
            time.sleep(10)
        elif i == 1:
            data['logs'].append('start verify os ....')
            data['status']['dowload_os']= 'success'
            data['status']['verify_os']= 'pending'
            redis.set(request_id, json.dumps(data))
            time.sleep(10)
        elif i == 2:
            data['logs'].append('start restore os ....')
            data['status']['verify_os']= 'success'
            data['status']['restore']= 'pending'
            redis.set(request_id, json.dumps(data))
            time.sleep(10)
        elif i == 3:
            data['logs'].append('completed!')
            data['status']['restore']= 'success'
            data['status']['general']= 'success'
            redis.set(request_id, json.dumps(data))
            
            
            
            
            