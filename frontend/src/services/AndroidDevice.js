import axios from "axios";


const BASE_URL = 'http://localhost:8081/api/'


// Upload image
export function GetDeviceList() {

    const promise = axios.get(
        BASE_URL + 'v1/android/device/info/list',
        {
            headers: {
                'accept': 'application/json'
            },
        }
    )
    const dataPromise = promise.then((response) => response.data)
    return dataPromise
}