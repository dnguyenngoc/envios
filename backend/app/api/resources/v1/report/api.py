from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter()


@router.get('/{pdf_name}', name='Get Report by pdf name')
async def get_pdf(pdf_name: str):
    print('[REPORT]')
    print('   - Get file: ', pdf_name + '.pdf')
    def iterfile():  
        with open('./storage/pdf/'+pdf_name, 'rb') as file_like:
            yield from file_like 
    return StreamingResponse(iterfile(), media_type="application/pdf")


@router.get('/{type}/{pdf_name}', name='Get Report by pdf folder')
async def get_pdf(type: str, pdf_name: str):
    print('[REPORT]')
    print('   - Get file: ', pdf_name + '.pdf')
    def iterfile():  
        with open('./storage/pdf/' + type + '/' + pdf_name, 'rb') as file_like:
            yield from file_like 
    return StreamingResponse(iterfile(), media_type="application/pdf")


