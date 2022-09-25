# import
from fastapi import APIRouter
from fastapi import HTTPException
import time
import uuid
from utils.time import now_utc
import subprocess


router = APIRouter()

list_key = ['UniqueDeviceID', 'UniqueChipID', 'TimeZone', 'SerialNumber', 'RegionInfo', 'ProductVersion', 'ProductType', 'ProductName', 'HardwareModel', 'DeviceColor', 'DeviceName','ActivationState', 'ProductName']


# time.sleep(2)
# end = []
# for i in range(5):
#     start_time = now_utc().timestamp()
#     request_id = str(uuid.uuid5(uuid.NAMESPACE_OID, "restore" + str(i) + str(start_time)))
#     end.append(
#     {
#         'DeviceId': 'device_id_'+str(i),
#         'RequestId': request_id,
#         'DeviceName': 'iPhone 8' + str(i),
#         "ActivationState": "Activated",
#         "DeviceClass": 'iPhone' + str(i),
#         'DeviceColor': 1,
#         'PhoneNumber': '+840123456789',
#         'ProductName': 'iPhone OS',
#         'ProductType': 'iPhone9,4',
#         'ProductVersion': '15.6.1',
#         'RegionInfo': 'LL/A',
#         'SIMStatus': 'Activated',
#         'SerialNumber': '44230ae2542',
#         'TimeZone': 'Asia/Ho_Chi_Minh',
#     })
    
# return end
@router.get('/info/list')
async def get_list_device():

    rst = subprocess.Popen(["idevice_id"], stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
    stdout, stderr = rst.stdout, rst.stderr
    data = []
    check = True
    for line in stderr:
        _str = line.decode('utf-8')
        if _str.__contains__("ERROR"):
            check = False
    if check == False:
        raise HTTPException(status_code=404, detail = 'Not found Device')

    for line in stdout:
        _str = line.decode('utf-8')
        device_id = _str.split()[0]
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
    return data
    
        

#  {
#     "DeviceId": device_id,
#     "ActivationState": "Activated",
#     "DeviceClass": 'iPhone',
#     'DeviceColor': 1,
#     'DeviceName': 'iPhone of Boss',
#     'PhoneNumber': '+840123456789',
#     'ProductName': 'iPhone OS',
#     'ProductType': 'iPhone9,4',
#     'ProductVersion': '15.6.1',
#     'RegionInfo': 'LL/A',
#     'SIMStatus': 'Activated',
#     'SerialNumber': '44230ae2542',
#     'TimeZone': 'Asia/Ho_Chi_Minh',
# }

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
