# 1. Install Libimobile
sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y libcurl4-openssl-dev libplist-dev libzip-dev openssl libssl-dev libusb-1.0-0-dev \
        libreadline-dev build-essential git make automake libtool pkg-config git python3-pip gunicorn

git clone https://github.com/libimobiledevice/libimobiledevice-glue
git clone https://github.com/libimobiledevice/libplist
git clone https://github.com/libimobiledevice/libusbmuxd
git clone https://github.com/libimobiledevice/usbmuxd
git clone https://github.com/libimobiledevice/libirecovery
git clone https://github.com/libimobiledevice/idevicerestore
git clone https://github.com/libimobiledevice/libimobiledevice

cd libimobiledevice-glue && git pull && ./autogen.sh && ./configure && sudo make install && cd ..
cd libplist && git pull && git checkout c3af449543795ad4d3ab178120ff69e90fdd2cc8 && ./autogen.sh && ./configure && ./configure && sudo make install && cd ..
cd libusbmuxd && git pull && git checkout 6426362e5cbad7284368b7fe70363f6b3251f94c && ./autogen.sh && ./configure && sudo make install && cd ..
cd libimobiledevice && git pull && git checkout b314f04bd791b263cf43fadc6ac0756e67ab4ed0 && ./autogen.sh && ./configure && sudo make install && cd ..
cd usbmuxd && git pull && git checkout bccae83d475ac5a48441001cad3fa8c167ecbb80 && ./autogen.sh && ./configure && sudo make install && cd ..
cd libirecovery && git pull && ./autogen.sh && ./configure && sudo make install && cd ..
cd idevicerestore && git pull && ./autogen.sh && ./configure && sudo make install && cd ..

sudo ldconfig

# 1.1 install lib for android
sudo apt install android-tools-adb android-tools-fastboot -y

## 2. Re-pull git repo
git pull

## 3. Install requirement python
pip3 install -r ./backend/requirements.txt

## 4. Install Nodejs and npm dependency
sudo apt install nodejs npm -y
cd frontend && npm install && cd ..