import uuid
import subprocess
from fastapi import APIRouter, HTTPException
from utils.time import now_utc


router = APIRouter()


def request_uuid(device_id):
        start_time = now_utc().timestamp()
        request_id = str(uuid.uuid5(uuid.NAMESPACE_OID, "restore-android" + device_id + str(start_time)))
        return request_id
    
    
@router.get('/info/list')
async def get_list_device():
    


    print('------------------------\n [LIST-DEVICE]')
    rst = subprocess.Popen(["adb", "devices", "-l"], stdout=subprocess.PIPE,  stderr=subprocess.STDOUT)
    stdout  = rst.stdout
    data = []
    
    
    count = 0
    for line in stdout:
        _str = line.decode('utf-8')
        _str = _str.replace("  ", " ")

        if _str.__contains__('List of devices attached') or _str.startswith("\n"):
            continue
            
        count +=1

        device_id = _str.split(" ")[0]
        request_id = request_uuid(device_id) 

        # Try to get device infor of each device in list idevice
        print('   - {}: get Info'.format(device_id))
        
        try:
            info = subprocess.Popen(["adb", "-s", "%s" %(device_id), "shell", "getprop"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout = info.stdout
        except Exception as e:
            print('[ERROR] Can not get device info by ideviceinfo?' + e)
            continue
    
        # Create default data even thought can't get baterry on device info
        _data = {}
        _data['device_id'] = device_id 
        _data['reequest_id']= request_id
        _data['battery.serial_number'] = ''
        _data['battery.manufacture_date'] = ''
        _data['battery.cycle_count'] = ''
        _data['battery.max_capacity'] = ''
        _data['battery.maximum_charge_current'] = ''
        
        for line in stdout:
            _str = line.decode('utf-8')
            _str = _str.split(":")
            
            if len(_str) > 1:
                key = _str[0]
                key = key.replace("[", "").replace("]", "")
                val = "".join(_str[1:])
                val = val.replace('\n', '').replace("[", "").replace("]", "")
                if val[0] == " ":
                    val = val[1:]
                if key.startswith("ro.product."):
                    _data[key] = val
                elif key.startswith("ro.build."):
                    if key == 'ro.build.version.release':
                        _data[key] = "Android " + val
                    else:
                        _data[key] = val
        data.append(_data)

    if count == 0:
        raise HTTPException(status_code=404, detail='Not found')
    
    return data
    
    
    
