from multiprocessing.context import ForkProcess
from fastapi import APIRouter, HTTPException, Form
from utils.time import now_utc
from settings import config
from utils.file import load_file
import subprocess
import time


router = APIRouter()


@router.post('/mode/')
async def change(*,
           request_id: str = Form(...),
           device_id: str = Form(...),
           type: str = Form('normal')):
    print('[CHANG-MODE]')
    if type == 'normal' or type == 'dfu': 
        pass
    else:
        raise HTTPException(status_code=400, detail='Not support this type: ' + type)
    json_path= config.STORAGE_DEFAULT_PATH + 'json/{}_{}.json'.format(request_id, device_id)
    try:
        info = load_file(json_path)
        chip_id = info['UniqueChipID']
    except:
        raise HTTPException(status_code=400, detail='not-found json file')
    
    data = {
            'request_id': request_id,
            'device_id': device_id,
            'type': type,
            'times':{
                'start': now_utc().timestamp(),
                'end': None,
            },
            'status': 'pending',
            'logs': [],
            'error': []
    }    
    try:
        if type == 'dfu':
            process = subprocess.Popen(["ideviceenterrecovery", "{}".format(device_id)], 
                                        stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
        elif type == 'normal':
            process = subprocess.Popen(["irecovery","-i", "{}".format(chip_id) , "-n"], 
                                        stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
        count= 0
        check_error = False
        while True:
            if count >= 5:
                break
            output = process.stdout.readline()
            if output:
                log = output.strip()
                str_log = log.decode('utf-8')
                if str_log.startswith('ERROR: Unable to connect') and type == 'normal':
                    check_error = True
                    data['logs'].append('Change mode to normal pass. Maybe device have been normal')
                    count += 10
                elif str_log.startswith('Failed to enter recovery mode.') and type == 'dfu':
                    data['logs'].append('Change mode to dfu failed')
                    check_error = True
                    count += 10
                elif str_log.startswith("No device found with udid"):
                    check_error = True
                    data['logs'].append('Change mode to dfu pass. Maybe device have been dfu')
                    count += 10
              
                    
                print(str_log)
            else:
                count += 10
            time.sleep(1)
            count+=1
        process.poll()
        if check_error:
            data['status'] = 'failed'
        else:
            data['status'] = 'success'
        data['times']['end'] = now_utc().timestamp()
        print('    + {} {} change_mode completed!'.format(request_id, device_id))
    except Exception as e:
        data['status'] = 'failed'
        data['error'].append(str(e))
        data['logs'].append(str(e))
        data['times']['end'] = now_utc().timestamp()
        print('    + {} {} change_mode failed!'.format(request_id, device_id))
    finally:
        if type == 'normal':
            time.sleep(20)
        else:
            time.sleep(5)
        return data