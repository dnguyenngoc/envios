kill -9 $(lsof -t -i tcp:8080)
cd frontend && npm run start