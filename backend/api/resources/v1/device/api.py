# import
from fastapi import APIRouter
from fastapi import HTTPException
import time
import uuid
from utils.time import now_utc


router = APIRouter()


@router.get('/info/list')
def get_list_device():
    try:
        time.sleep(2)
        end = []
        for i in range(5):
            start_time = now_utc().timestamp()
            request_id = str(uuid.uuid5(uuid.NAMESPACE_OID, "restore" + str(i) + str(start_time)))
            end.append(
            {
                'DeviceId': 'device_id_'+str(i),
                'RequestId': request_id,
                'DeviceName': 'iPhone 8' + str(i),
                "ActivationState": "Activated",
                "DeviceClass": 'iPhone' + str(i),
                'DeviceColor': 1,
                'PhoneNumber': '+840123456789',
                'ProductName': 'iPhone OS',
                'ProductType': 'iPhone9,4',
                'ProductVersion': '15.6.1',
                'RegionInfo': 'LL/A',
                'SIMStatus': 'Activated',
                'SerialNumber': '44230ae2542',
                'TimeZone': 'Asia/Ho_Chi_Minh',
            })
          
        return end
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/info/{device_id}")
def restore(device_id: str):
    return {
        "DeviceId": device_id,
        "ActivationState": "Activated",
        "DeviceClass": 'iPhone',
        'DeviceColor': 1,
        'DeviceName': 'iPhone of Boss',
        'PhoneNumber': '+840123456789',
        'ProductName': 'iPhone OS',
        'ProductType': 'iPhone9,4',
        'ProductVersion': '15.6.1',
        'RegionInfo': 'LL/A',
        'SIMStatus': 'Activated',
        'SerialNumber': '44230ae2542',
        'TimeZone': 'Asia/Ho_Chi_Minh',
    }
