import axios from "axios";


const BASE_URL = 'http://localhost:8081/api/'


export function RunRestore(deviceId, requestId) {
    const promise = axios.post(
        BASE_URL + `v1/restore/process/${deviceId}/${requestId}`,
        {
            headers: {
                'accept': 'application/json'
            },
        }
    )
    const dataPromise = promise.then((response) => response.data)
    return dataPromise
}


// Get status by TaskId
export async function GetStatus(requestId) {
    const promise = await axios({
        timeout: 3000,
        url: BASE_URL + `v1/restore/status/${requestId}`,
        method: 'get',
        headers: { 'accept': 'application/json' }
      }
    )
    return promise
}

export async function GetStatusFull(requestIds) {
    const temp = await Promise.all(requestIds.map(async (element) => {
        const post = await GetStatus(element);
        return post.data
    }));
    return temp
}

export async function GetStatusList(requestIds){
    var data = JSON.stringify({"requests": requestIds});
      var config = {
        method: 'post',
        url: BASE_URL + 'v1/restore/status/',
        headers: { 
          'Content-Type': 'application/json'
        },
        data : data
      };
      try {
        const data = await axios(config);
        return data;
      } catch (e) {
        console.log(e)
      }
}
