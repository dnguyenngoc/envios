from fastapi import APIRouter
from fastapi import HTTPException
import uuid
import json

from utils.time import now_utc
from utils.file import save_file, is_exists
from settings import config
import regex
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
        
        product_type = ''
        
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
                product_type = val.replace('\n', '')
                _data['ActualProductType'] = config.APPLE_PRODUCT_TYPE[product_type]
            _data[key] = val.replace('\n', '')
        
        if product_type.startswith('iPhone'):
            p_type_ver = float(product_type.split('iPhone')[-1].replace(',', '.'))
            if p_type_ver <= 9.4:
                 # Get battery info
                print("   - [GET-Battery] process..")
                try:
                    battery = subprocess.Popen(["idevicediagnostics", 'ioregentry', 'AppleARMPMUCharger', "-u", "{}".format(device_id)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    battery_stdout = battery.stdout
                    lines = list(battery_stdout)
            
                    x = {}
                    x['BatterySerialNumber'] = None
                    x['BatteryManufactureDate'] = None
                    x['BatteryCycleCount'] = None
                    x['BatteryMaxCapacity'] = None
                    x['BatteryMaximumChargeCurrent'] = None
                
                    for i, line in enumerate(lines):
                        str_line = line.decode('utf-8')
                        if (str_line.__contains__('BatterySerialNumber') or str_line.__contains__('<key>Serial</key>')) and x['BatterySerialNumber']== None:
                            x['BatterySerialNumber'] = i+1
                        elif str_line.__contains__('CycleCount') and x['BatteryCycleCount']== None:
                            x['BatteryCycleCount'] = i+1
                        elif str_line.__contains__('ManufactureDate'):
                            x['BatteryManufactureDate'] = i+1
                        elif str_line.__contains__('MaxCapacity') and x['BatteryMaxCapacity']==None:
                            x['BatteryMaxCapacity'] = i+1
                        elif str_line.__contains__('MaximumChargeCurrent'):
                            x['BatteryMaximumChargeCurrent'] = i+1
                    for key, val in x.items():
                        if val != None:
                            t_data  = regex.search('\>([A-Za-z0-9]+)\<', lines[val].decode('utf-8')).groups()
                            _data[key] = t_data[0]
                        else:
                            _data[key] = ''
                    print("   - [GET-Battery] Success", x)
                except Exception as e:
                    print("   - [GET-Battery] ERROR", e) 
            else:
                pass
        
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
