import { Button } from 'antd';
import React, { useState, memo } from 'react';
import { Document, Page,pdfjs } from 'react-pdf';
import './pdf.scss'


const Pdf = ({rName, funcCloseReport}) => {
    let url = `http://localhost:8081/api/v1/report/${rName}`

    pdfjs.GlobalWorkerOptions.workerSrc = 
    `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);

    function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
    setPageNumber(1);
    }

    return (
        <div className='carousel__wrapper'>
            <div style={{display: 'inline-flex', width: '100%'}}>
                <p style={{marginLeft: '10px'}}>Report: {rName}</p>
                <Button style={{float: 'right', left: '370px', backgroundColor:'#FF4136'}} type='text' onClick={funcCloseReport}>X</Button>
            </div>
            <div className="carousel__container">
            <Document
                    file={url}
                    onLoadSuccess={onDocumentLoadSuccess}
                >
                    <Page pageNumber={pageNumber} />
            </Document> 
            </div>
          
           
        </div>

    )
}


export default memo(Pdf);