from fastapi import APIRouter
from api.resources.v1.restore import api as r_restore
from api.resources.v1.device import api as r_device
from api.resources.v1.report import api as r_report


router = APIRouter()


router.include_router(r_device.router, prefix="/device",  tags=["V1-DEVICE"])
router.include_router(r_restore.router, prefix="/restore",  tags=["V1-RESTORE"])
router.include_router(r_report.router, prefix="/report",  tags=["V1-REPORT"])
