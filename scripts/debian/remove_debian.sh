cd idevicerestore && sudo make uninstall && cd ..
cd libirecovery && sudo make uninstall && cd ..
cd libplist && sudo make uninstall && cd ..
cd libusbmuxd && sudo make uninstall && cd ..
cd libimobiledevice-glue && sudo make uninstall && cd ..
cd libimobiledevice && sudo make uninstall && cd ..
cd usbmuxd && sudo make uninstall && cd ..

rm -rf idevicerestore libirecovery libplist libusbmuxd libimobiledevice-glue libimobiledevice usbmuxd
