sudo port install -y libimobiledevice
sudo port install -y idevicerestore
sudo port install -y android-platform-tools
sudo port install -y nodejs18
sudo port install -y npm9

git pull

pip3 install -r ./backend/requirements.txt
cd ./frontend && npm install && cd ..