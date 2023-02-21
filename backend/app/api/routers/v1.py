from fastapi import APIRouter

from api.resources.v1.device import android as android_r_device
from api.resources.v1.restore import android as android_r_restore

from api.resources.v1.device import ios as ios_r_device
from api.resources.v1.restore import ios as ios_r_restore
from api.resources.v1.device import ios_mode as ios_r_mode_device


from api.resources.v1.status import api as r_status
from api.resources.v1.report import api as r_report


router = APIRouter()


router.include_router(r_status.router, prefix="/status",  tags=["V1-STATUS"])


router.include_router(android_r_device.router, prefix="/android/device",  tags=["V1-ANDROID"])
router.include_router(android_r_restore.router, prefix="/android/restore",  tags=["V1-ANDROID"])


router.include_router(ios_r_device.router, prefix="/ios/device",  tags=["V1-IOS"])
router.include_router(ios_r_mode_device.router, prefix="/ios/device",  tags=["V1-IOS"])
router.include_router(ios_r_restore.router, prefix="/ios/restore",  tags=["V1-IOS"])


router.include_router(r_report.router, prefix="/report",  tags=["V1-REPORT"])
