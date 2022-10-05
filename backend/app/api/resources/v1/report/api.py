from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter()


@router.get('/{pdf_name}')
async def get_pdf(pdf_name: str):
    print('[REPORT]')
    print('   - Get file: ', pdf_name + '.pdf')
    def iterfile():  
        with open('./storage/pdf/'+pdf_name, 'rb') as file_like:
            yield from file_like 
    return StreamingResponse(iterfile(), media_type="application/pdf")


