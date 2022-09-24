# virtualenv venv
# source ../venv/bin/activate
pip3 install -r ./requirements.txt

gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8081


# uvicorn main:app --host 0.0.0.0 --port 8081 --reload