
import json
from utils.file import save_file
from utils.time import now_utc
from init import redis
import json
import subprocess
import time
from utils.report import make_report, create_hardware_info, create_erasure_info
from utils.file import load_file
from settings import config


def restore_process(request_id: str, device_id: str):
    data = {
            'request_id': request_id,
            'device_id': device_id,
            'times':{
                'start': now_utc().timestamp(),
                'end': None,
            },
            'status':{
                'general': 'pending',
                'dowload_os': 'pending',
                'verify_os': None,
                'extracting_filesystem': None,
                'sending_filesystem': None,
                'restore': None
            },
            'logs': ["run cmd idevicerestore -e -l -y -u {}".format(device_id)],
            'error': [],
            'new_os': ''
    }
    redis.set(request_id, json.dumps(data))
    time.sleep(2)
    data['logs'].append('dowload os .........')
    redis.set(request_id, json.dumps(data))
    
    try:
        process = subprocess.Popen(["idevicerestore", "-e","-l", "-y" ,"-u", "{}".format(device_id)], 
                                    stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
        
        check_error = False
        stop_loop = False
        count= 0
        while True:
            print('[{}] in while loop ...'.format(request_id))
            if count == 3:
                data['error'].append('ERROR: Unable to receive message from FDR')
                data['logs'].append('ERROR: Unable to receive message from FDR')
                redis.set(request_id, json.dumps(data))
                break
            output = process.stdout.readline()
            if output:
                log = output.strip()
                str_log = log.decode('utf-8')
                if str_log.startswith('ERROR: Unable to receive message from FDR'):
                    count += 1
                elif str_log.startswith("ERROR"):
                    check_error = True
                    data['error'].append(str_log)
                elif str_log.startswith("Product Version:"):
                    data['new_os'] = str_log.split(': ')[-1]
                elif str_log.startswith('Getting ApNonce in normal mode'):
                    data['status']['dowload_os'] = 'success'
                    data['status']['verify_os'] = 'success'
                    data['status']['extracting_filesystem'] = 'success'
                elif str_log.startswith('Done sending filesystem'):
                    data['status']['sending_filesystem'] = 'success'
                elif str_log.startswith('Status: Restore Finished') or str_log.startswith('DONE'):
                    data['status']['restore'] = 'success'
                    stop_loop = True
                data['logs'].append(str_log)
                redis.set(request_id, json.dumps(data))
                print('[{}] {}'.format(request_id, str_log))
                if check_error or stop_loop:
                    break
            else:
                print("Dont have any output ..")
        process.poll()

        if check_error:
            data['status']['general'] = 'failed'
        elif stop_loop:
            data['status']['general'] = 'success'
        data['times']['end'] = now_utc().timestamp()
        redis.set(request_id, json.dumps(data))
        print('[{}] Done!'.format(request_id))
        
    except Exception as e:
        data['status']['general'] = 'failed'
        data['error'].append(str(e))
        data['logs'].append(str(e))
        data['times']['end'] = now_utc().timestamp()
        redis.set(request_id, json.dumps(data))
    finally:
        save_file(config.STORAGE_DEFAULT_PATH + 'data_logs/{}.json'.format(request_id + '_' + device_id), data)
        print('[{}] Save logs file success'.format(request_id))
        
        info = load_file(config.STORAGE_DEFAULT_PATH + '{type}/{name}.{type}'.format(type = 'json', name = request_id + '_' + device_id))
        text_erasure = create_erasure_info(data, info)
        text_hardware = create_hardware_info(info)
        data = {}
        data['erasure'] = text_erasure
        data['hardware_detail'] = text_hardware
        #         text_battery = """Serial:
# Manufacturing Date:
# Recharge Cycles:
# Capacity:
# Wear Level:
# Charge Level:
# Health Level:
# Temperature:
# Apple Health Metric:
#         """
        # data['battery_info'] = text_battery
        make_report(info['SerialNumber'], data) 
        print('[{}] Make report success'.format(request_id))
        
        
                
            
            
            
            
            