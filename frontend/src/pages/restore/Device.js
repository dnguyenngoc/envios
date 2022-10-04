import { memo, useEffect, useState, useRef } from "react";
import Done from '../../assets/images/svg/done.svg'
import Fail from '../../assets/images/svg/fail.svg'
import SpinLoading from '../../components/loadings/SpinLoading'
import { Button, Input} from 'antd';
import * as apiRestoreService from '../../services/Restore';
import * as apiDeviceService from '../../services/Device';



const { TextArea } = Input;


export default memo(
  function Device({ ids, infos, handleInprocess}){
    const styles = {
      device: {boxShadow: 'rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px',
               height: '100px', width: '100%', marginTop: '30px', display: 'inline-flex', padding: '5px 5px'},
      deviceInfo: {display: 'block', width: '20%', listStyleType: 'none'},
      restoreLogs: {marginRight: '35px', marginLeft: '15px', display: 'block', width: '60%'},
      restoreStatus: {width: '20%',marginRight: '25px',textAlign: 'center',alignItems: 'center',display: 'flex'},
      button: {marginRight: '30px'},
      siconStatus: {width: '20px',},
      info:{fontSize: '10px', padding: '0px 10px'}
    }
    
   
    // Status of button
    const [statusB, setStatusB] = useState([])
    const [mode, setMode] = useState([])
    const [logs, setLogs] = useState([])
    const [status, setStatus] = useState([])
    const [startTime, setStartTime] = useState([])
    const [running, setRunning] = useState(0)


    // need change only one state if you want to increase performace
    useEffect(() => {
      setMode(ids.map(item => ('normal')));
      setStatusB(ids.map(item => false));
      setLogs(ids.map(item=> ('')));
      setStatus(ids.map(item=> ('not-start')));
    }, [ids]);

    let ref  = useRef(null);

    function isDone(element) {
      return element !== 'pending';
    }

    useEffect(() => {
      if (running > 0){
        handleInprocess(true)
        ref.current = setInterval(async() => { // Trigger each 7s to get status of request.
          let stemp = [...status]
          let sbtemp = [...statusB]
          let slogs = [...logs]

          var requestIds  = []
          status.forEach((item, i) => {requestIds.push(infos[i].RequestID)})
          // console.log("Request_IDs:", requestIds)

          await apiRestoreService.GetStatusList(requestIds)
          .then(res => { 
            res.data.map((item, i) => {
              stemp[i] = item.status.general
              slogs[i] = item.logs.at(-1)
              
              if (item.status.general === 'success') {
                sbtemp[i] = false
              }else if (item.status.general === 'failed'){
                sbtemp[i] = false
              }else{
                sbtemp[i] = true
              }
              return null
            })
          })
          .catch(e=> {
            console.log(e)
          })
          setStatus(stemp)
          setStatusB(sbtemp)
          setLogs(slogs)
          
          if (stemp.every(isDone)) {
            clearInterval(ref.current) // Stop the interval if the condition holds true
            setRunning(0)
            handleInprocess(false)
          }
        }, 13000);
      }
      else {
        clearInterval(ref.current); // Stop the interval if the condition holds true

      }
      return () => {
        clearInterval(ref.current); // unmount coponent
      };
    }, [running, infos, status, statusB, logs, handleInprocess])

    
    // trigger api to start restore
    async function funcRestore(i){
      apiRestoreService.RunRestore(infos[i].DeviceId, infos[i].RequestID)
      .then(res => {
          let sTime = [...startTime]
          sTime[i] = res.time_request
          setStartTime(sTime)
      })
      .catch(e => {
        console.log(e)
    })

      let newArr = [...statusB];
      let newLogs = [...logs];
      let newStatus = [...status];

      newStatus[i] = 'pending'
      newLogs[i] = 'Starting restore phone ....'
      newArr[i] = true;


      setLogs(newLogs)
      setStatusB(newArr)
      setStatus(newStatus)
      setRunning(running+1)
      
    }

    // const sleep = (milliseconds) => {
    //   return new Promise(resolve => setTimeout(resolve, milliseconds))
    // }

    // function handle logs
    function funcUpdateLog(i, message){
      var tempLogs = [...logs]
      tempLogs[i] = message
      setLogs(tempLogs)
    }

    // Change mode
    async function funcChangeMode(i){
      var tempMode = [...mode]
      var tempMode1 = [...mode]

      tempMode1[i] = 'pending'
      setMode(tempMode1)

      if (tempMode[i] === 'normal' || tempMode[i] === 'dfu'){
        const type = tempMode[i]
        var runType = type
        if (type === 'normal') runType ='dfu'
        else runType = 'normal'

        await apiDeviceService.ChangeMode(infos[i]['RequestID'], infos[i]['DeviceId'], runType)
        .then(res => {
          console.log(res)
          if (res.status === 'success'){ 
            tempMode[i] = res.type
            funcUpdateLog(i, 'Device is successfully switching to ' + res.type )
          }else {
            tempMode[i] = type
            funcUpdateLog(i, 'ERROR: Unable to discover device mode. Please make sure a device is attached.')
          }
        })
        .catch(e=> {
          tempMode[i] = type
        })
        .finally(e => {
          setMode(tempMode)
          }
        )
      }
    }

    // Status of restore device
    const Status =(sta) => {
        if (sta === 'not-start' || sta === undefined) return <></>
        else if (sta === 'pending') return <SpinLoading/>
        else if (sta === 'success') return <img src={Done} alt='' style={styles.siconStatus}></img>
        else return <img src={Fail} alt='' style={styles.siconStatus}></img>
    }

    return(<div>
      {ids.map((id, i) => {
        return (
          <div key={i} style={styles.device}>
            <div style={styles.deviceInfo}>
              <li style={styles.info}><b>DeviceName:</b> {infos[i].DeviceName}</li>
              <li style={styles.info}><b>ActivationState:</b> {infos[i].ActivationState}</li>
              <li style={styles.info}><b>ProductVersion:</b> {infos[i].ProductVersion}</li>
              <li style={styles.info}><b>DeviceColor:</b> {infos[i].DeviceColor}</li>
              <li style={styles.info}><b>RequestId:</b> {infos[i].RequestID}</li>

            </div>
            <div style={styles.restoreLogs}>
              <TextArea
                placeholder="Logs of process"
                  className="custom"
                  style={{height: 80, maxHeight: 80}}
                  value={logs[i]}
              />
            </div>
            <div style={styles.restoreStatus}>
                    <Button disabled={mode[i] === 'pending' || statusB[i] ? true : false} onClick={()=> funcChangeMode(i)} type="info" size='large' style={styles.button}>{mode[i]}</Button>

                    <Button disabled={statusB[i]} onClick={()=> funcRestore(i)} type="danger" size='large' style={styles.button}>Restore</Button>
                    {Status(status[i])}
                </div>
            </div>
                )
             })
            }
        </div>)
    }
)