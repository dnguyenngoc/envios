import React from 'react';
import Logo from '../../assets/images/logo/envios.png';
import {  Dropdown, Space, Menu } from 'antd';
import { DownOutlined } from '@ant-design/icons';


const menu = (
    <Menu>
        <Menu.Item>
            <a rel="noopener noreferrer" href="/tool/ios-restore">IOS Restore</a>
        </Menu.Item>
        <Menu.Item>
            <a rel="noopener noreferrer" href="/tool/android-restore">Android Restore</a>
        </Menu.Item>
    </Menu>
);


const Header = () => {
      
    return (
    <div style={{    
        position: 'absolute',
        backgroundColor: 'transparent',
        zIndex: 100,
        top: 0,
        left: 0,
        right: 0,
        height: '120px',
    }}>
        <div style={{ paddingTop: '20px', paddingLeft: '40px'}}>
            <a style={{float: 'left'}} href='/'>
                <img src={Logo} style={{width:'140px', boxShadow: 'rgba(0, 0, 0, 0.4) 0px 2px 4px, rgba(0, 0, 0, 0.3) 0px 7px 13px -3px, rgba(0, 0, 0, 0.2) 0px -3px 0px inset'}} alt=''></img>
            </a>
            <div style={{float: 'right', paddingRight: '100px', paddingTop:'10px'}}>
                <div style={{
                    display: 'flex',
                    fontSize: '35px',
                    listStyleType: 'none',
                }}>
                    <Dropdown
                        overlay={menu}
                        trigger={['hover']}
                    >
                        <a onClick={(e) => e.preventDefault()}>
                        <Space>
                            Restores
                            {/* <DownOutlined /> */}
                        </Space>
                        </a>
                    </Dropdown>
                    <a href='/not-found'><li style={{color: 'black', paddingLeft: "20px"}}>About Us</li></a>
                </div>
            </div>
        </div>
       
     </div>
    )
}

export default Header;
