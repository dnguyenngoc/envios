import React, { useState } from 'react';
import { Button, Alert } from 'antd';
import BackGround from '../assets/images/bg/2.png'
import Device from './restore/Device';
import * as apiDeviceService from '../services/Device'
import SpinLoading from '../components/loadings/SpinLoading';



const Restore = () => {
  const styles = {
    page: {backgroundImage: `url(${BackGround})`,height: '100%',backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',backgroundSize: 'cover',minHeight: '100vh',paddingTop: '170px'},
    form: {padding: '5px 10px',margin: '0 auto',minHeight: '900px',width: '80%'},
    titles: {display: 'inline-flex',textAlign: 'center',alignItems: 'center',},
    title: {color: '#ACB0C8',fontSize: '40px',fontFamily: 'sans-serif',fontWeight: 'bold',
        margin: '0 auto',paddingRight: '20px'},
    }

    const [infos, setInfos] = useState([])
    const [ids, setIds] = useState([])
    const [getDevicesButton, setGetDevicesButton] = useState(false)
    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState(null)

    const funcGetDevices = () => {
        setMessage(null)
        setGetDevicesButton(true)
        setLoading(true)
        apiDeviceService.GetDeviceList()
          .then(res => {
            setInfos(res)
            let ids = res.map((_,i) => {
              return i
            })
            setIds(ids)
            setLoading(false)

          })
          .catch(e => {
            if (e.response.status === 404){
              setGetDevicesButton(false)
              setMessage('Device Not Found')
            }
            setLoading(false)
        })
    }

    const funcStopAllProcess = () => {
        setInfos([])
        setIds([])
        setLoading(false)
        setGetDevicesButton(false)
        setMessage(null)
        setInterval(false)
    }
    
    return (
        <div style={styles.page}>

            <div style={styles.form}>
                <div style={styles.titles}>
                    <h5 style={styles.title}>List of DEVICE</h5>
                    <Button disabled={getDevicesButton} onClick={funcGetDevices} type="primary" shape="round" size='large' style={{boxShadow: 'rgba(6, 24, 44, 0.4) 0px 0px 0px 2px, rgba(6, 24, 44, 0.65) 0px 4px 6px -1px, rgba(255, 255, 255, 0.08) 0px 1px 0px inset', color:'black'}}>Get Devices</Button>
                    <Button onClick={funcStopAllProcess} type="primary" shape="round" size='large' style={{boxShadow: 'rgba(6, 24, 44, 0.4) 0px 0px 0px 2px, rgba(6, 24, 44, 0.65) 0px 4px 6px -1px, rgba(255, 255, 255, 0.08) 0px 1px 0px inset', color:'black', marginLeft: '20px'}}>Stop All Process</Button>
                    {loading ?<div style={{paddingLeft: '30px', paddingTop: '5px'}}><SpinLoading/></div> : ''}
                    {message !== null ? <Alert message={message} type="warning" showIcon closable style={{marginLeft: '30px'}} /> : ""}

                </div>
                {getDevicesButton === true ? 
                <Device
                  ids={ids}
                  infos={infos} 
                />
                : ""}
            </div>
        </div>
    )
}

export default Restore;
