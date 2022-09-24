import React from 'react';
import Logo from '../../assets/images/logo/envios.png';


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
        <div style={{ paddingTop: '20px', paddingLeft: '50px'}}>
            <a style={{float: 'left'}} href='/'>
                <img src={Logo} style={{width:'140px', boxShadow: 'rgba(0, 0, 0, 0.4) 0px 2px 4px, rgba(0, 0, 0, 0.3) 0px 7px 13px -3px, rgba(0, 0, 0, 0.2) 0px -3px 0px inset'}} alt=''></img>
            </a>
            <div style={{float: 'right', paddingRight: '100px', paddingTop:'10px'}}>
                <div style={{
                    display: 'flex',
                    fontSize: '35px',
                    listStyleType: 'none',
                }}>
                    <a href='/restore'><li style={{paddingRight: '20px', color: 'black'}}>Features</li></a>
                    <a href='/not-found'><li style={{color: 'black'}}>About Us</li></a>
                </div>
            </div>
        </div>
       
     </div>
    )
}

export default Header;
