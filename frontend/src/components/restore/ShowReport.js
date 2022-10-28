import { memo } from "react";
import Pdf from '../pdfviews/pdf';


export default memo(function ShowReport({isShowReport, reportNameShow, funcCloseReport}){
    return <>
      {isShowReport ? <Pdf rName = {reportNameShow} funcCloseReport={funcCloseReport}/> : ''}
    </>
})