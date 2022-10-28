kill -9 $(lsof -t -i tcp:8081)
# cd backend/app && pip3 install -r ../requirements.txt  && gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8081
cd backend/app && pip3 install -r ../requirements.txt && uvicorn main:app --host 0.0.0.0 --port 8081 --reload