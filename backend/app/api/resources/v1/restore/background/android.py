
import json
from utils.file import save_file
from utils.time import now_utc
from init import redis
import json
import time
from utils.android_report import make_report
from utils.file import load_file
from settings import config


def restore_process(request_id: str, device_id: str, report_name: str):
    
    json_path= config.STORAGE_DEFAULT_PATH + 'json/{}_{}.json'.format(request_id, device_id)
    
    info = load_file(json_path)
        
    if report_name == '.pdf':
        report_name = info['device_id'] + '_' + info['ro.product.odm.brand'] + '_' + info['ro.product.odm.device'] + '.pdf'
    else:
        report_name = report_name[:-4]
        
    data = {
            'request_id': request_id,
            'device_id': device_id,
            'times':{
                'start': now_utc().timestamp(),
                'end': None,
            },
            'progress': {
                'name': '',
                'step': 0,
                'percent': 0,
                'status': True,
            },
            'status':{
                'general': 'pending',
                'get_product': 'pending',
                'get_battery': None,
                'get_system': None,
                'make_report': None,
            },
            'logs': ["start process {}".format(device_id)],
            'error': [],
            'new_os': ''
    }
    redis.set(request_id, json.dumps(data))
    
    try:
        print('[{}] in while loop ...'.format(request_id))
    
        data['progress']['name'] = 'Get Info of product'
        data['progress']['percent'] = 20
        data['logs'].append('Get Info of product -> Done')
        data['status']['get_product'] = 'success'
        redis.set(request_id, json.dumps(data))
        time.sleep(2)
        
        data['progress']['name'] = 'Get Info of battery'
        data['progress']['percent'] = 50
        data['logs'].append('Get Info of battery -> Done')
        data['status']['get_battery'] = 'success'
        redis.set(request_id, json.dumps(data))
        time.sleep(2)
        
        data['progress']['name'] = 'Get info of System'
        data['progress']['percent'] = 70
        data['logs'].append('Get Info of System -> Done')
        data['status']['get_system'] = 'success'
        redis.set(request_id, json.dumps(data))
        time.sleep(2)
        
        data['progress']['name'] = 'Make Report'
        data['progress']['percent'] = 90
        data['logs'].append('Make Report -> Done')
        data['status']['make_report'] = 'success'
        redis.set(request_id, json.dumps(data))
        time.sleep(2)
        
        data['new_os'] = "Android 11"
        data['progress']['status'] = True
        data['progress']['percent'] = 100
        data['progress']['step'] = 12
        data['progress']['name'] = 'Completed!'
        data['times']['end'] = now_utc().timestamp()
        data['status']['general'] = 'success'
        redis.set(request_id, json.dumps(data))
        print('[{}] Done!'.format(request_id))
        
    except Exception as e:
        data['progress']['status'] = False
        data['progress']['percent'] = 50
        data['status']['general'] = 'failed'
        data['error'].append(str(e))
        data['logs'].append(str(e))
        data['times']['end'] = now_utc().timestamp()
        redis.set(request_id, json.dumps(data))
        
    finally:
        save_file(config.STORAGE_DEFAULT_PATH + 'data_logs/{}.json'.format(request_id + '_' + device_id), data)
        print('[{}] Save logs file success'.format(request_id))
        make_report(report_name, data, info) 
        print('[{}] Make report {} success'.format(request_id, report_name+ '.pdf'))
        