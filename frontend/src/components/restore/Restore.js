import React, { useState, useCallback, useEffect } from 'react'
import classes from './Restore.module.css'
import { deleteProcess, deleteRestore } from '../../features/RestoreSlide'
import { useDispatch } from 'react-redux'
import { Button, Input } from 'antd';
import ShowReport from './ShowReport';
import { addProcess } from '../../features/RestoreSlide'
import { useSelector } from "react-redux";
import * as apiRestoreService from '../../services/Restore';
import * as apiDeviceService from '../../services/Device';


const Restore = ({ restore: {id, info} }) => {
  const dispatch = useDispatch();
  const [isShowReport, setIsShowReport] = useState(false)
  const [reportNameShow, setReportNameShow] = useState('')
  const [reportName, setReportName] = useState(info.SerialNumber + '.pdf')
  const [isRunning, setIsRunning] = useState(false)

  const process = useSelector((state) => state.restores.process[id]);

  useEffect(() => {
    // console.log(process)
    if (process === undefined) {
        setIsRunning(false)
    }else {
        
    }
  }, [process]);


  const submitRestore = () => {
    setIsRunning(true)
    apiRestoreService.RunRestore(info.DeviceId, info.RequestID, reportName)
      .then(res => {
        console.log(res)
      })
      .catch(e => {
         alert('Can not trigger Restore', id)
      })

    const request = {
        requestId: info.RequestID,
        deviceId: id,
        status: 'pending',
    }
    dispatch(addProcess(request))
  }

  // Function close report
  const funcCloseReport = useCallback(() => {
    setIsShowReport(false)
    setReportNameShow('')
  }, [])

  // Show report
  const showReport = ()  => {
    setReportNameShow(reportName)
    setIsShowReport(true)
  }

  // Change report name
  const funcChangeReportName = (e) => setReportName(e.target.value)

  // fuction close device
  const closeDevice = () => {
    dispatch(deleteRestore(id))
    dispatch(deleteProcess(id))
  }
  
  return (
    <div key={id} className={classes.device}>
      <ShowReport reportNameShow={reportNameShow} isShowReport={isShowReport} funcCloseReport={funcCloseReport}></ShowReport>
      <div className={classes.deviceInfo}>
        <li className={classes.info}><b>DeviceName:</b> {info.DeviceName}</li>
        <li className={classes.info}><b>DeviceType:</b> {info.ActualProductType}</li>
        <li className={classes.info}><b>ProductVersion:</b> {info.ProductVersion}</li>
        <li className={classes.info}><b>ActivationState:</b> {info.ActivationState}</li> 
        <li className={classes.info}><b>DeviceColor:</b> {info.DeviceColor}</li>
      </div>

      <div className={classes.restoreStatus}>
        <div style={{display: 'grid',  marginRight: '15px'}}>
          {/* <Button disabled={mode[i] === 'pending' || statusB[i] ? true : false} onClick={()=> funcChangeMode(i)} type="primary" size='normal' style={styles.button}>{mode[i]}</Button> */}
          <Button type="danger" disabled={isRunning} size='normal' className={classes.button} onClick={submitRestore}>Restore</Button>
        </div>
            
            {/* {Status(status[i])} */}

        </div>

      <div className={classes.restoreReport}>
        <h5 className={classes.restoreReportTitle}>Report Name</h5>
        <Input value={reportName} onChange={e => funcChangeReportName(e)} size='normal'/>
      </div>

      <div className={classes.reportClose}>
        <Button type="ghost" size='normal' onClick={closeDevice} className={classes.button}>X</Button>
        <Button onClick={showReport} type="primary" size='normal' className={classes.button}>View Report</Button>
      </div>

    </div>
  )
}

export default Restore;