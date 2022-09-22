# import
from fastapi import APIRouter
from fastapi import HTTPException


router = APIRouter()


@router.get('/list')
def get_list_device():
    try:
        end = ['usb_1', 'usb_2']
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
