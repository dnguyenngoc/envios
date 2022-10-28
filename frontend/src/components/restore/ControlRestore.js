import React, { useState } from 'react'
import classes from './ControlRestore.module.css'
import { useDispatch } from 'react-redux'
import { Button } from 'antd';
import * as apiDeviceService from '../../services/Device'
// import * as apiRestoreService from '../../services/Restore'
import SpinLoading from '../loadings/SpinLoading';
import BackGround from '../../assets/images/bg/2.png'
import { updateRestore } from '../../features/RestoreSlide'

const ControlRestore = () => {
  const [loading, setLoading] = useState(false)
  // const [lockButtonAll, setLockButonAll] = useState(false)
  // const [lockButtonRemove, setLockButonRemove] = useState(true)

  const dispatch = useDispatch();


  const submitUpdateRestore = (e) => {
      e.preventDefault();
      setLoading(true)
      apiDeviceService.GetDeviceList()
	      .then(res => {
	        let action = res.map((data) => {
	          return {
              id: data.DeviceId,
              info: data
            }
	        })
          // Create newListDevices get from 
          dispatch(updateRestore(action))
      })
      .catch(e => {
        if (e.response.status === 404){
          alert('Not Found Device!')
        } else {
          alert('Backend Error!')
        }
    })
    setLoading(false)
  }

  return (
    <div className={classes.page} style={{backgroundImage: `url(${BackGround})`}} >
	  <div className={classes.form}>
		<div className={classes.titles}>
		  <h5 className={classes.title}>List of DEVICE</h5>
			<Button 
        onClick={submitUpdateRestore} 
        type="primary" 
        shape="round" 
        size='large' 
        className={classes.bntget}>
        Get Devices
      </Button>
			{loading ?<div className={classes.loading}><SpinLoading/></div> : ''}
		</div>
	  </div>
	</div>
  )
}

export default ControlRestore;