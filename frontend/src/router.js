
import { Route, Routes } from "react-router-dom";

import NotFound from "./components/responses/NotFound.js";
import Header from "./components/headers/HeaderV1.js";

import Restore from './pages/Restore'
import RestoreRedux from './pages/RestoreRedux'
import Home from './pages/Home.js'


const RoutesInit = () => {
    // const auth = isAuth()
    return (
      <>
      <Header/>
      <Routes>
         <Route path='/' element={<Home/>} />
         <Route path='/tool/restore' element={<Restore/>} />
         <Route path='/tool/restore-redux' element={<RestoreRedux/>} />
         {/* <Route path='/account' element={<ProtectedRoute  authed={auth} component={<Account/>}/>} /> */}
         <Route path='*' element={<NotFound />} />
      </Routes>
      {/* <Footer/> */}
      </>
    );
  };

  export default RoutesInit