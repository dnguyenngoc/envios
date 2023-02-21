
import { Route, Routes } from "react-router-dom";

import NotFound from "./components/responses/NotFound.js";
import Header from "./components/headers/HeaderV1.js";

import IOSRestore from './pages/IOSRestore'
import AndroidRestore from './pages/AndroidRestore'
import Home from './pages/Home.js'


const RoutesInit = () => {
    // const auth = isAuth()
    return (
      <>
      <Header/>
      <Routes>
         <Route path='/' element={<Home/>} />
         <Route path='/tool/ios-restore' element={<IOSRestore/>} />
         <Route path='/tool/android-restore' element={<AndroidRestore/>} />
         {/* <Route path='/account' element={<ProtectedRoute  authed={auth} component={<Account/>}/>} /> */}
         <Route path='*' element={<NotFound />} />
      </Routes>
      {/* <Footer/> */}
      </>
    );
  };

  export default RoutesInit