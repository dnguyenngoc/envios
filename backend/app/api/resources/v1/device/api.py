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


class Device:
    
    def _request_uuid(self, device_id):
        start_time = now_utc().timestamp()
        request_id = str(uuid.uuid5(uuid.NAMESPACE_OID, "restore" + device_id + str(start_time)))
        return request_id
    
    def _actual_product_type(self, product_type):
        try:
            data = config.APPLE_PRODUCT_TYPE[product_type]
            return data
        except:
            return None
        
device = Device()


@router.get('/info/list')
async def get_list_device():
    print('------------------------\n [LIST-DEVICE]')
    rst = subprocess.Popen(["idevice_id"], stdout=subprocess.PIPE,  stderr=subprocess.STDOUT)
    stdout  = rst.stdout
    data = []
    for line in stdout:
        _str = line.decode('utf-8')
        
        # Raise HTTP 404 not found when command check device list error
        if _str.__contains__("ERROR"):
            raise HTTPException(status_code=404, detail='Not found')

        # make device and request_id
        device_id = _str.split()[0]
        request_id = device._request_uuid(device_id) 
               
        # Try to get device infor of each device in list idevice
        print('   - {}: get Info'.format(device_id))
        try:
            info = subprocess.Popen(["ideviceinfo", "-u", "{}".format(device_id)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout = info.stdout
        except Exception as e:
            print('[ERROR] Can not get device info by ideviceinfo?' + e)
            continue
        
        # Create default data even thought can't get baterry on device info
        _data = {}
        _data['DeviceId'] = device_id 
        _data['ActualProductType'] = None
        _data['RequestID']= request_id
        _data['BatterySerialNumber'] = ''
        _data['BatteryManufactureDate'] = ''
        _data['BatteryCycleCount'] = ''
        _data['BatteryMaxCapacity'] = ''
        _data['BatteryMaximumChargeCurrent'] = ''
        
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
            
            # using config apple type to get actual productType
            if key == 'ProductType': 
                product_type = val.replace('\n', '')
                _data['ActualProductType'] = device._actual_product_type(product_type)
            
            # update other data key, value base on result of ideviceinfo    
            _data[key] = val.replace('\n', '')
        
        if product_type.startswith('iPhone'):
            p_type_ver = float(product_type.split('iPhone')[-1].replace(',', '.'))
            if p_type_ver <= 9.4:
                
                 # Get battery info
                print("   - [GET-Battery] process..")
                try:
                    temp = {}
                    temp['BatterySerialNumber'] = None
                    temp['BatteryManufactureDate'] = None
                    temp['BatteryCycleCount'] = None
                    temp['BatteryMaxCapacity'] = None
                    temp['BatteryMaximumChargeCurrent'] = None
                    
                    battery = subprocess.Popen(["idevicediagnostics", 'ioregentry', 'AppleARMPMUCharger', "-u", "{}".format(device_id)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    battery_stdout = battery.stdout
                    lines = list(battery_stdout)
                    # print(lines)
                    for i, line in enumerate(lines):
                        str_line = line.decode('utf-8')
                        if (str_line.__contains__('BatterySerialNumber') or str_line.__contains__('<key>Serial</key>')) and temp['BatterySerialNumber']== None:
                            temp['BatterySerialNumber'] = i+1
                        elif str_line.__contains__('CycleCount') and temp['BatteryCycleCount']== None:
                            temp['BatteryCycleCount'] = i+1
                        elif str_line.__contains__('ManufactureDate'):
                            temp['BatteryManufactureDate'] = i+1
                        elif str_line.__contains__('MaxCapacity') and temp['BatteryMaxCapacity']==None:
                            temp['BatteryMaxCapacity'] = i+1
                        elif str_line.__contains__('MaximumChargeCurrent'):
                            temp['BatteryMaximumChargeCurrent'] = i+1
                            
                    for key, val in temp.items():
                        if val != None:
                            t_data  = regex.search('\>([A-Za-z0-9]+)\<', lines[val].decode('utf-8')).groups()
                            _data[key] = t_data[0]
                        else:
                            _data[key] = ''
                        print(f"   - [GET-Battery] {key} -> {_data[key]}")
                
                except Exception as e:
                    print("   - [GET-Battery] ERROR", e) 
            else:
                print((f"   - [GET-Battery] not support for {_data['ActualProductType']} now!") )
        
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
