import React, { useState } from 'react';
import { Document, Page,pdfjs } from 'react-pdf';
import './pdf.scss'


const Pdf = ({rName}) => {
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
            <div>Report: {rName}</div>
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


export default Pdf;