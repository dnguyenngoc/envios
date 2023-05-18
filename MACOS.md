## 1. Need install xcode

Run command and follow this link [Install-Xcode](https://www.freecodecamp.org/news/install-xcode-command-line-tools/)

```
brew install git
xcode-select --install
```

Check if the Code has been generated successfully.

```
xcode-select -p
```

Show result ```/Applications/Xcode.app/Contents/Developer```


## 2. Instart Macports
The macport is management tool alternative for brew. 

### a. Install mports base
Pick a location to store a working copy of the MacPorts code. For this example, ```/opt/mports``` will be used, but you can put the source anywhere. This example will create ```/opt/mports/macports-base``` containing everything needed for MacPorts.

```
sudo mkdir -p /opt/mports
cd /opt/mports
sudo git clone https://github.com/macports/macports-base.git
sudo git checkout v2.7.2
cd macports-base
cd /opt/mports/macports-base
sudo ./configure --enable-readline
sudo make
sudo make install
sudo make distclean
```

### b. Instart mports-ports
- Configure MacPorts to use port information from Git. This step is useful if you want to do port development. Check out the ports tree from git

```
cd /opt/mports
sudo git clone https://github.com/macports/macports-ports.git
```

Then open ```/opt/local/etc/macports/sources.conf``` in a text editor. The last line should look like this:

```
nano /opt/local/etc/macports/sources.conf
```
Change last line ```rsync://rsync.macports.org/macports/release/tarballs/ports.tar [default]``` with ```file:///opt/mports/macports-ports [default]```


### c. Add mports to PATH
```
echo -n 'export PATH=/opt/local/bin:/opt/local/sbin:$PATH' >> ~/.zshrc
echo -n 'export PATH=/opt/local/bin:/opt/local/sbin:$PATH' >> ~/.bashrc
```

### d. Update mports
```
sudo port -d selfupdate
```

## 3. Build App
```
sudo sh scripts/macos/build.sh
```

## 4. Start App

Open 2 `terminal` and run each `terminal` with command like bellow:

```
sudo sh scripts/run/be.sh
```
```
sudo sh scripts/run/fe.sh
```
and goto `http://localhost:8080/`