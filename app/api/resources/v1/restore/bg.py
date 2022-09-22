import json
from utils.time import now_utc
from init import redis
import json
import logging


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
            'general': 'success',
            'dowload_os': 'success',
            'verify_os': 'success',
            'restore': 'success'
        },
        'error': None
    }
    redis.set(request_id, json.dumps(data))
    print('{} - [Restore] r: {}, d: {} - Completed!'.format(now_utc(), request_id, device_id))