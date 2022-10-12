import { memo, useEffect, useState, useRef } from "react";
import Done from '../../assets/images/svg/done.svg'
import Fail from '../../assets/images/svg/fail.svg'
import SpinLoading from '../../components/loadings/SpinLoading'
import { Button, Input, Progress} from 'antd';
import { red, green } from '@ant-design/colors';
import * as apiRestoreService from '../../services/Restore';
import * as apiDeviceService from '../../services/Device';
import Pdf from "../../components/pdfviews/pdf";



const { TextArea } = Input;


export default memo(
  function Device({ ids, infos, handleInprocess}){
    const styles = {
      device: {boxShadow: 'rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px',
               height: '100px', width: '100%', marginTop: '30px', display: 'inline-flex', padding: '5px 5px', background: 'white'},
      deviceInfo: {display: 'block', width: '20%', listStyleType: 'none'},
      restoreLogs: {marginRight: '35px', marginLeft: '15px', display: 'block', width: '42%'},
      restoreReport:  {marginRight: '25px', marginLeft: '2px', display: 'block', width: '18%', padding: '5px'},
      restoreStatus: {width: '20%',marginRight: '25px',textAlign: 'center',alignItems: 'center',display: 'flex'},
      button: {marginRight: '30px', margin: '3px 3px'},
      siconStatus: {width: '20px'},
      info:{fontSize: '10px', padding: '0px 10px'},
      restoreReportTitle: {fontSize: '11px'}
    }
    
   
    // Status of button
    const [statusB, setStatusB] = useState([])
    const [mode, setMode] = useState([])
    const [logs, setLogs] = useState([])
    const [status, setStatus] = useState([])
    const [startTime, setStartTime] = useState([])
    const [running, setRunning] = useState(0)
    const [reportName, setReportName] = useState([])
    const [isShowReport, setIsShowReport] = useState(false)
    const [reportNameShow, setReportNameShow] = useState('')
    const [steps, setSteps] = useState([])
    const [processColors, setProcessColors] = useState([])


    // need change only one state if you want to increase performace
    useEffect(() => {
      setSteps(infos.map(item=> ({step: 0, percent: 0, name: '', status: true})));
      setProcessColors(infos.map(item => ([green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6]])))
      setMode(ids.map(item => ('normal')));
      setStatusB(ids.map(item => false));
      setLogs(ids.map(item=> ('')));
      setStatus(ids.map(item=> ('not-start')));
      setReportName(infos.map(item=> (item.SerialNumber + '.pdf')));
    }, [ids, infos]);
    // console.log(steps)

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
          let stepsTemp = [...steps]
          let processColorsTemp = [...processColors]

          var requestIds  = []
          status.forEach((item, i) => {requestIds.push(infos[i].RequestID)})
          // console.log("Request_IDs:", requestIds)

          await apiRestoreService.GetStatusList(requestIds)
          .then(res => { 
            console.log(res)
            res.data.map((item, i) => {
              stemp[i] = item.status.general
              slogs[i] = item.logs.at(-1)
              stepsTemp[i] = item.progress
              let tempx = [red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5]]

              if (item.progress.status === true){
                tempx = [green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6]]
              }else{
                tempx = [red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5],red[5]]
              }
              processColorsTemp[i] = tempx
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
          setSteps(stepsTemp)
          setProcessColors(processColorsTemp)
          
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
    }, [running, infos, status, statusB, logs, handleInprocess, processColors, steps])

    
    // trigger api to start restore
    async function funcRestore(i){
      apiRestoreService.RunRestore(infos[i].DeviceId, infos[i].RequestID, reportName[i])
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
      let stepsTemp = [...steps];
      let processColorsTemp = [...processColors]

      stepsTemp[i] = {step: 0, percent: 0, name: '', status: true}
      newStatus[i] = 'pending'
      newLogs[i] = 'Starting restore phone ....'
      newArr[i] = true;
      processColorsTemp[i] = [green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6],green[6]]



      setLogs(newLogs)
      setStatusB(newArr)
      setStatus(newStatus)
      setRunning(running+1)
      setSteps(stepsTemp)
      setProcessColors(processColorsTemp)
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

    // Change report name
    function funcChangeReportName(e, i){
      var tempRpn = [...reportName]
      if (e.target.value.endsWith('.pdf')){
        tempRpn[i] = e.target.value
      }
      setReportName(tempRpn)
    }

    //Function show report
    function funcShowReport(i) {
      if (isShowReport){
        setIsShowReport(false)
        setReportNameShow('')
      }else{
        let data = reportName[i]
        setReportNameShow(data)
        setIsShowReport(true)
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
            {isShowReport ? <Pdf rName = {reportNameShow}/> : ''}
            <div style={styles.deviceInfo}>
              <li style={styles.info}><b>DeviceName:</b> {infos[i].DeviceName}</li>
              <li style={styles.info}><b>DeviceType:</b> {infos[i].ActualProductType}</li>
              <li style={styles.info}><b>ProductVersion:</b> {infos[i].ProductVersion}</li>
              <li style={styles.info}><b>ActivationState:</b> {infos[i].ActivationState}</li> 
              <li style={styles.info}><b>DeviceColor:</b> {infos[i].DeviceColor}</li>
            </div>
            <div style={styles.restoreLogs}>
              <TextArea
                placeholder="Logs of process"
                  className="custom"
                  style={{height: 80, maxHeight: 60}}
                  value={logs[i]}
              />
             
              {steps[i] !== undefined ?
                <div style={{display: 'inline-flex', height: '20px'}}>
                <Progress style={{paddingTop: '4px'}} percent={steps[i].percent} steps={12} strokeColor={processColors[i]} />
                <p style={{paddingLeft: '10px'}}>{steps[i].name}</p>
              </div>
                : ''
              }
              
            </div>
            <div style={styles.restoreReport}>
              <h5 style={styles.restoreReportTitle}>Report Name</h5>
              <Input value={reportName[i]} onChange={e => funcChangeReportName(e, i)} size='normal'/>
            </div>
            <div style={styles.restoreStatus}>
                <div style={{display:'grid',  marginRight: '15px'}}>
                  <Button disabled={mode[i] === 'pending' || statusB[i] ? true : false} onClick={()=> funcChangeMode(i)} type="primary" size='normal' style={styles.button}>{mode[i]}</Button>
                  <Button disabled={statusB[i]} onClick={()=> funcRestore(i)} type="danger" size='normal' style={styles.button}>Restore</Button>
                </div>
                
                {Status(status[i])}

               </div>
               <div style={{float: 'left'}}>
               <Button onClick={()=> funcShowReport(i)} type="primary" size='normal' style={styles.button}>View Report</Button>
               {/* <Button onClick={()=> funcShowReport(i)} type="primary" size='normal' style={styles.button}>Stop</Button> */}
               </div>

            </div>
                )
             })
            }
        

        </div>)
    }
)