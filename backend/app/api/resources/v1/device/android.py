import uuid
import subprocess
from fastapi import APIRouter, HTTPException
from utils.time import now_utc
from settings import config
from utils.file import save_file


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
        _data['request_id']= request_id
        _data['battery.technology'] = ''
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
                if key == "wlan.mac.address":
                    val = ":".join(_str[1:])
                else:
                    val = "".join(_str[1:])
                val = val.replace('\n', '').replace("[", "").replace("]", "")
                if val[0] == " ":
                    val = val[1:]
                if key.startswith("ro.product.") or key.startswith("ro.vendor."):
                    _data[key] = val
                elif key.startswith("ro.build."):
                    if key == 'ro.build.version.release':
                        _data[key] = "Android " + val
                    else:
                        _data[key] = val
                elif key.startswith("wlan."):
                    _data[key] = val
                elif key.startswith("ro.serialno") \
                    or key.startswith("persist.sys.timezone") \
                    or key.startswith("ro.hardware") \
                    or key.startswith('mediatek.wlan.chip'):
                    _data[key] = val
                elif key.startswith("ro.config.") or key.startswith("net.bt."):
                    _data[key] = val

        # Update battery info
        try:
            info = subprocess.Popen(["adb", "-s", "%s" %(device_id), "shell", "dumpsys", "battery"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout = info.stdout
            for line in stdout:
                _str = line.decode('utf-8')
                _str = _str.split(":")
                if _str[0].__contains__("technology"):
                    _data['battery.technology'] = _str[1].replace("\n", "")
                elif _str[0].__contains__("LLB CAL"):
                    _data['battery.manufacture_date'] = _str[1].replace("\n", "")
                elif _str[0].__contains__("mSavedBatteryMaxCurrent"):
                    _data['battery.cycle_count'] = _str[1].replace("\n", "")
                elif _str[0].__contains__("mSavedBatteryUsage"):
                    _data['battery.max_capacity'] = _str[1].replace("\n", "")
                elif _str[0].__contains__("mSavedBatteryAsoc"):
                    _data['battery.maximum_charge_current'] = _str[1].replace("\n", "")
        except Exception as e:
            print(e)
            pass
        
        save_file(config.STORAGE_DEFAULT_PATH + 'json/%s%s' %(request_id + '_' + device_id, '.json'), _data)
        
        data.append(_data)

    if count == 0:
        raise HTTPException(status_code=404, detail='Not found')
    
    return data
    
    
    
