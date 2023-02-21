import axios from "axios";


const BASE_URL = 'http://localhost:8081/api/'


export function RunRestore(deviceId, requestId, reportName) {
  var formData = new FormData()
  formData.append('request_id', requestId)
  formData.append('device_id', deviceId)
  formData.append('report_name', reportName)
  var config = {
    method: 'post',
    url: BASE_URL + 'v1/android/restore/process/',
    headers: { 
    },
    data : formData
  };
  const promise = axios(config)
  const dataPromise = promise.then((response) => response.data)
  return dataPromise
}

export async function GetStatusList(requestIds){
    var data = JSON.stringify({"requests": requestIds});
      var config = {
        method: 'post',
        url: BASE_URL + 'v1/status/',
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
    url: BASE_URL +  `v1/restore/remove-all-bg/?filter=${filter}`,
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