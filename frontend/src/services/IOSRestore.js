import axios from "axios";


const BASE_URL = 'http://localhost:8081/api/'


export function RunRestore(deviceId, requestId, reportName) {
  var formData = new FormData()
  formData.append('request_id', requestId)
  formData.append('device_id', deviceId)
  formData.append('report_name', reportName)
  var config = {
    method: 'post',
    url: BASE_URL + 'v1/ios/restore/process/',
    headers: { 
    },
    data : formData
  };
  const promise = axios(config)
  const dataPromise = promise.then((response) => response.data)
  return dataPromise
}


// Get status by TaskId
export async function GetStatus(requestId) {
    const promise = await axios({
        timeout: 3000,
        url: BASE_URL + `v1/ios/restore/status/${requestId}`,
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
        url: BASE_URL + 'v1/ios/restore/status/',
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

export function StopAllProcess(filter){
  var config = {
    method: 'post',
    url: BASE_URL +  `v1/ios/restore/remove-all-bg/?filter=${filter}`,
    headers: { 
      'Content-Type': 'application/json'
    },
  }
  axios(config);
}

export function removeLogs(filter){
  var config = {
    method: 'post',
    url: BASE_URL +  `v1/ios/restore/remove-all-logs/`,
    headers: { 
      'Content-Type': 'application/json'
    },
  }
  axios(config);
}