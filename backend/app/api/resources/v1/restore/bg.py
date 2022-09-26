import json
from utils.time import now_utc
from init import redis
import json
import subprocess
import time

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
            'error': []
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

        
            
            
            
            
            