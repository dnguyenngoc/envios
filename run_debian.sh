
sudo kill -9 $(lsof -t -i tcp:8081)
sudo kill -9 $(lsof -t -i tcp:8080)

cd frontend && npm run start & 
cd backend/app && pip3 install -r requirements.txt  && gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8081
