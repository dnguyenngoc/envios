kill -9 $(lsof -t -i tcp:8081) & 
kill -9 $(lsof -t -i tcp:8080) &