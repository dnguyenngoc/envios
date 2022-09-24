import React from 'react';
import { Button } from 'antd';
import BackGround from '../assets/images/bg/1.png'
import PiLogo from '../assets/images/logo/delete.png'


const Home = () => {

    const styles = {
        homepage: {
            backgroundImage: `url(${BackGround})`,
            height: '100%', 
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            backgroundSize: 'cover',
            minHeight: '100vh'
        },
        hpContent: {
            minWidth: '500px',
            maxWidth: '1200px',
            paddingTop: '20%',
            paddingLeft: '10%',
        },
        title: {
            display: 'flex'
        },
        titleImage: {
            marginBottom: '10px',
            paddingLeft: '5px',
            width: '70px',
            height: 'auto'
        },
        titleText: {
            fontSize: '65px',
            fontWeight: 'bold',
            font: 'Roboto'
        }
    }
    return (
    <div style={styles.homepage}>
        <div style={styles.hpContent}>
            <div style={styles.title}>
                <h5 style={styles.titleText}> Deleting all iPhones that are plug in via USB
                    <img style={styles.titleImage} alt='' src = {PiLogo}></img>
                </h5>
            </div>
            <Button type="primary" shape="round" size='large' href='/tool/restore'
                style={{ 
                    background: "#F76540",
                    borderColor: "#F76540", 
                    width: '170px',
                    fontSize: '18px',
                    fontWeight: 'bold',
                    }}>
                Try Now
            </Button>
        </div>
       
    </div>
    )
}

export default Home;
