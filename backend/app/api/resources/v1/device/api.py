from fastapi import APIRouter
from fastapi import HTTPException
import uuid
from utils.time import now_utc
import subprocess
import sh


router = APIRouter()


list_key = ['UniqueDeviceID', 'UniqueChipID', 'TimeZone', 'SerialNumber', 'RegionInfo', 'ProductVersion', 'ProductType', 'ProductName', 'HardwareModel', 'DeviceColor', 'DeviceName','ActivationState', 'ProductName']


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
        info = subprocess.Popen(["ideviceinfo", "-u", "{}".format(device_id)], stdout=subprocess.PIPE)
        stdout = info.stdout
        _data = {'DeviceId': device_id}
        start_time = now_utc().timestamp()
        request_id = str(uuid.uuid5(uuid.NAMESPACE_OID, "restore" + device_id + str(start_time)))
        _data['RequestID']= request_id
        for line in stdout:
            _str = line.decode('utf-8')
            _str = _str.split(": ")
            key = _str[0]
            val = _str[1]
            if key in list_key:
                _data[key] = val.replace('\n', '')
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
        key = _str[0]
        val = _str[1]
        if key in list_key:
            _data[key] = val.replace('\n', '')
    return _data
