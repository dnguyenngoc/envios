import React from 'react'
import { useRef, useEffect } from 'react';
import Restore from './Restore'
import classes from './Restores.module.css'
import { useSelector } from "react-redux";



export default function Restores({restores}){

  let ref = useRef(null)

  const process = useSelector((state) => state.restores.process);
  
  // useEffect(() => {
  //   if (process !== {}) {
  //     ref.current = setInterval(async() => { // Trigger each 7s to get status of request.
  //       let status = []
  //       let statusButton = []
  //       let logs = []
  //       let steps = []
  //       var requestIds  = []
  //       // process.forEach((key, val) => {requestIds.push(val.RequestID)})
  //       console.log("Request_IDs:", requestIds)
  //     })
  //   }

  // }, 13000);
    //     await apiRestoreService.GetStatusList(requestIds)
    //     .then(res => { 
    //       console.log(res)
    //       res.data.map((item, i) => {
    //         stemp[i] = item.status.general
    //         slogs[i] = item.logs.at(-1)
    //         stepsTemp[i] = item.progress
    //         let tempx = [red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5]]

    //         if (item.progress.status === true){
    //           tempx = [green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6]]
    //         }else{
    //           tempx = [red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5]]
    //         }
    //         processColorsTemp[i] = tempx
    //         if (item.status.general === 'success') {
    //           sbtemp[i] = false
    //         }else if (item.status.general === 'failed'){
    //           sbtemp[i] = false
    //         }else{
    //           sbtemp[i] = true
    //         }
    //         return null
    //       })
    //     })
    //     .catch(e=> {
    //       console.log(e)
    //     })
    //     setStatus(stemp)
    //     setStatusB(sbtemp)
    //     setLogs(slogs)
    //     setSteps(stepsTemp)
    //     setProcessColors(processColorsTemp)
        
    //     if (stemp.every(isDone)) {
    //       clearInterval(ref.current) // Stop the interval if the condition holds true
    //       setRunning(0)
    //       handleInprocess(false)

   
  
  return(
    <div className={classes.restores}>
      { restores.map((restore) => (
          <Restore key={restore.id} restore={restore} requests/>
      ))
      }
    </div>
  ) 
}
