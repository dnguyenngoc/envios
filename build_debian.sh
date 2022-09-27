# 1. Install Libimobile
sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y libcurl4-openssl-dev libplist-dev libzip-dev openssl libssl-dev libusb-1.0-0-dev \
        libreadline-dev build-essential git make automake libtool pkg-config git

git clone https://github.com/libimobiledevice/libimobiledevice-glue
git clone https://github.com/libimobiledevice/libplist
git clone https://github.com/libimobiledevice/libusbmuxd
git clone https://github.com/libimobiledevice/usbmuxd
git clone https://github.com/libimobiledevice/libirecovery
git clone https://github.com/libimobiledevice/idevicerestore
git clone https://github.com/libimobiledevice/libimobiledevice

cd libimobiledevice-glue && git pull && ./autogen.sh && ./configure && sudo make install && cd ..
cd libplist && git pull && ./autogen.sh && ./configure && ./configure && sudo make install && cd ..
cd libusbmuxd && git pull && ./autogen.sh && ./configure && sudo make install && cd ..
cd libimobiledevice && git pull && ./autogen.sh && ./configure && sudo make install && cd ..
cd usbmuxd && git pull && ./autogen.sh && ./configure && sudo make install && cd ..
cd libirecovery && git pull && ./autogen.sh && ./configure && sudo make install && cd ..
cd idevicerestore && git pull && ./autogen.sh && ./configure && sudo make install && cd ..

sudo ldconfig


## 2. Install requirement python
pip3 install -r ./backend/requirements.txt

## 3. Install Nodejs and npm dependency
sudo apt install nodejs npm -y
cd frontend && npm install



