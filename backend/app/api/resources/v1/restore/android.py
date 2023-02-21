
# import
from fastapi import APIRouter, BackgroundTasks, Form
from utils.time import now_utc
from api.resources.v1.restore.background.android import restore_process


router = APIRouter()


@router.post("/process/")
async def restore(*,
                  device_id: str = Form(...), 
                  request_id: str = Form(...),
                  report_name: str = Form(...),
                  background_tasks: BackgroundTasks):

    # create request uuid
    start_time = now_utc().timestamp()
    
    # run process in backgroud
    background_tasks.add_task(restore_process, request_id, device_id, report_name)
    
    return {
        'time_request': start_time,
        'device_id': device_id,
        'request_id': request_id
    }