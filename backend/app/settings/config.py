import os
import datetime
import pytz



#======================================
# PROJECT-INFO CONFIG
#======================================
u = datetime.datetime.utcnow()
u = u.replace(tzinfo=pytz.timezone("Asia/Ho_Chi_Minh"))
PROJECT_NAME = 'envios'
CORS_MIDDLEWARE = '*'
