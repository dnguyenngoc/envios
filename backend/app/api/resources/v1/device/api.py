from fastapi import APIRouter
from fastapi import HTTPException
import uuid
from utils.time import now_utc
from utils.file import save_file, is_exists
from settings import config
import json

import subprocess


router = APIRouter()


# list_key = ['UniqueDeviceID', 'UniqueChipID', 'TimeZone', 'SerialNumber', 'RegionInfo', 'ProductVersion', 'ProductType', 'ProductName', 'HardwareModel', 'DeviceColor', 'DeviceName','ActivationState', 'ProductName']


@router.get('/info/list')
async def get_list_device():
    print('[LIST-DEVICE]')
    rst = subprocess.Popen(["idevice_id"], stdout=subprocess.PIPE,  stderr=subprocess.STDOUT)
    stdout  = rst.stdout
    data = []
    for line in stdout:
        _str = line.decode('utf-8')
        if _str.__contains__("ERROR"):
            raise HTTPException(status_code=404, detail='Not found')
        device_id = _str.split()[0]
        print('   - {}: get Info'.format(device_id))
        try:
            info = subprocess.Popen(["ideviceinfo", "-u", "{}".format(device_id)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout = info.stdout
        except Exception as e:
            print(e)
            continue
        _data = {'DeviceId': device_id}
        _data['ActualProductType'] = None
        start_time = now_utc().timestamp()
        request_id = str(uuid.uuid5(uuid.NAMESPACE_OID, "restore" + device_id + str(start_time)))
        _data['RequestID']= request_id
        _check = True
        for line in stdout:
            _str = line.decode('utf-8')
            if _str.startswith("ERROR"):
                print(_str)
                _check = False
            _str = _str.split(": ")
            key = _str[0]
            val = _str[1]
            if key == 'ProductType': # using config apple type to get actual productType
                _data['ActualProductType'] = config.APPLE_PRODUCT_TYPE[val.replace('\n', '')]
            _data[key] = val.replace('\n', '')
        if _check == True:
            save_file(config.STORAGE_DEFAULT_PATH + 'json/%s%s' %(request_id + '_' + device_id, '.json'), _data)
            data.append(_data)
    if len(data) == 0:
        raise HTTPException(status_code=404, detail='Not Found')
    print('\n')
    return data


@router.get("/info/{device_id}")
def restore(device_id: str):
    info = subprocess.Popen(["ideviceinfo", "-u", "{}".format(device_id)], stdout=subprocess.PIPE)
    stdout = info.stdout
    _data = {'DeviceId': device_id}
    for line in stdout:
        _str = line.decode('utf-8')
        _str = _str.split(": ")
        # key = _str[0]
        # val = _str[1]
        # if key in list_key:
        #     _data[key] = val.replace('\n', '')
    return _data


@router.get("/info/json/{request_id}/{device_id}")
def restore(request_id: str, device_id: str):
    path = config.STORAGE_DEFAULT_PATH + 'json/%s%s' %(request_id + '_' + device_id, '.json')
    if is_exists(path) == False:
        raise HTTPException(status_code=404, detail='Not Found')
    data = open(path, 'rb').read()
    data = json.loads(data)
    return data
