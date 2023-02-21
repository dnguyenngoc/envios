import axios from "axios";


const BASE_URL = 'http://localhost:8081/api/'


// Upload image
export function GetDeviceList() {

    const promise = axios.get(
        BASE_URL + 'v1/ios/device/info/list',
        {
            headers: {
                'accept': 'application/json'
            },
        }
    )
    const dataPromise = promise.then((response) => response.data)
    return dataPromise
}


// Change mode of device
export function ChangeMode(requestId, deviceId, type){
    var formData = new FormData()
    formData.append('request_id', requestId)
    formData.append('device_id', deviceId)
    formData.append('type', type)
    // console.log('formdata', formData)
    var config = {
        method: 'post',
        url: BASE_URL + 'v1/ios/device/mode/',
        headers: { 
        },
        data : formData
    };

    const promise = axios(config)
    const dataPromise = promise.then((response) => response.data)
    return dataPromise
}