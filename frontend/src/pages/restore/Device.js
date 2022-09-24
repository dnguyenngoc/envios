import { memo, useEffect, useState, useRef } from "react";
import Done from '../../assets/images/svg/done.svg'
import Fail from '../../assets/images/svg/fail.svg'
import SpinLoading from '../../components/loadings/SpinLoading'
import { Button, Input} from 'antd';
import * as apiRestoreService from '../../services/Restore';


const { TextArea } = Input;


export default memo(
  function Device({ ids, infos}){
    const styles = {
      device: {boxShadow: 'rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px',
               height: '100px', width: '100%', marginTop: '30px', display: 'inline-flex', padding: '5px 5px'},
      deviceInfo: {display: 'block', width: '20%', listStyleType: 'none',},
      restoreLogs: {marginRight: '35px', marginLeft: '15px', display: 'block', width: '60%'},
      restoreStatus: {width: '20%',marginRight: '25px',textAlign: 'center',alignItems: 'center',display: 'flex'},
      button: {marginRight: '30px'},
      siconStatus: {width: '20px',},
      info:{fontSize: '12px', padding: '0px 10px'}
    }
    
    // Status of button
    const [statusB, setStatusB] = useState(ids.map(item=>  {return false}))
    const [logs, setLogs] = useState(ids.map((item, i)=>  {return ''}))
    const [status, setStatus] = useState(ids.map((item, i)=>  {return 'not-start'}))
    const [startTime, setStartTime] = useState([])
    const [running, setRunning] = useState(0)


    let ref  = useRef(null);

    function isDone(element) {
      return element !== 'pending';
    }


    useEffect(() => {
      if (running > 0)
        ref.current = setInterval(async() => { // Trigger each 7s to get status of request.
          let stemp = [...status]
          let sbtemp = [...statusB]
          let slogs = [...logs]

          

          var requestIds  = []
          status.forEach((item, i) => {requestIds.push(infos[i].RequestId)})
          console.log("Request_IDs:", requestIds)

          await apiRestoreService.GetStatusList(requestIds)
          .then(res => { 
            res.data.map((item, i) => {
              stemp[i] = item.status.general
              console.log(item)
              slogs[i] = item.logs.at(-1)
              
              if (item.status.general === 'success') {
                sbtemp[i] = false
              }else if (item.status.general === 'failed'){
                sbtemp[i] = true
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

          }
        }, 7000);
      else clearInterval(ref.current); // Stop the interval if the condition holds true
      return () => {
        clearInterval(ref.current); // unmount coponent
      };
    }, [running, infos, status, statusB, logs])

    
    // trigger api to start restore
    async function funcRestore(i){
      apiRestoreService.RunRestore(infos[i].DeviceId, infos[i].RequestId)
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