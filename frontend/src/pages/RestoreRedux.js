import { useSelector } from "react-redux";
import classes from './RestoreRedux.module.css'
import BackGround from '../assets/images/bg/2.png'
import ControlRestore from "../components/restore/ControlRestore";
import Restores from "../components/restore/Restores";


function RestoreRedux() {

  const restores = useSelector((state) => state.restores.restores);

  return (
	<div className={classes.page} style={{backgroundImage: `url(${BackGround})`}} >
	  <ControlRestore/>
	  <Restores restores={restores}/>
	</div>
  );
}

export default RestoreRedux;