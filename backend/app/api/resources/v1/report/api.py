from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter()


@router.get('/{request_id}')
async def get_pdf(request_id: str):
    print('[REPORT]')
    print('   - Get file: ', request_id + '.pdf')
    def iterfile():  
        with open('./storage/pdf/'+request_id + '.pdf', 'rb') as file_like:
            yield from file_like 
    return StreamingResponse(iterfile(), media_type="application/pdf")


