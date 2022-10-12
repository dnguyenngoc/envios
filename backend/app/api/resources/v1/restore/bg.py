
import json
from utils.file import save_file
from utils.time import now_utc
from init import redis
import json
import subprocess
import time
from utils.report import make_report
from utils.file import load_file
from settings import config


def restore_process(request_id: str, device_id: str, report_name: str):
    
    json_path= config.STORAGE_DEFAULT_PATH + 'json/{}_{}.json'.format(request_id, device_id)
    info = load_file(json_path)
    chip_id = info['UniqueChipID']
    if report_name == '.pdf':
        report_name = info['SerialNumber']
    else:
        report_name = report_name[:-4]
    data = {
            'request_id': request_id,
            'device_id': device_id,
            'chip_id': chip_id,
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
                'dowload_os': 'pending',
                'verify_os': None,
                'extracting_filesystem': None,
                'sending_filesystem': None,
                'restore': None
            },
            'logs': ["run cmd idevicerestore -e -l -y -e {}".format(chip_id)],
            'error': [],
            'new_os': ''
    }
    redis.set(request_id, json.dumps(data))
    time.sleep(2)
    data['logs'].append('Please wait until the firmware is downloaded, it may take a long time due to the network ...')
    redis.set(request_id, json.dumps(data))
    
    try:
        process = subprocess.Popen(["idevicerestore", "--erase","--latest", "--no-input", "--plain-progress","--ecid", "{}".format(chip_id)], 
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
                if str_log.startswith('progress'): # handle process bar 'progress: 0 0.200000'
                    progress = str_log.split(" ")
                    progress_type, _ = int(progress[-2]), float(progress[-1])
                    if progress_type == 0:
                        data['progress']['name'] = 'Dowloading'
                        data['progress']['percent'] = 10
                    elif progress_type == 1:
                        data['progress']['name'] = 'Erasing'
                        data['progress']['percent'] = 20
                    elif progress_type == 2:
                        data['progress']['name'] = 'Erasing'
                        data['progress']['percent'] = 30
                    elif progress_type == 3:
                        data['progress']['name'] = 'Verifying restore'
                        data['progress']['percent'] = 50
                    elif progress_type == 4:
                        data['progress']['name'] = 'Flashing firmware'
                        data['progress']['percent'] = 60
                    elif time.process_time == 6:
                        data['progress']['name'] = 'Requesting FUD data'
                        data['progress']['percent'] = 70
                    data['progress']['step'] = progress_type+5
                elif str_log.startswith('ERROR: Unable to receive message from FDR'):
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
            data['progress']['status'] = False
        elif stop_loop:
            data['status']['general'] = 'success'
            data['progress']['status'] = True
            data['progress']['percent'] = 100
            data['progress']['step'] = 12
            data['progress']['name'] = 'Completed!'
        data['times']['end'] = now_utc().timestamp()
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
        info = load_file(config.STORAGE_DEFAULT_PATH + '{type}/{name}.{type}'.format(type = 'json', name = request_id + '_' + device_id))
        make_report(report_name, data, info) 
        print('[{}] Make report {} success'.format(request_id, report_name+ '.pdf'))
        
        
                
            
            
            
            
            