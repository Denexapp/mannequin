import time
import sys
import usb.core
import usb.util

class ups(object):
    def attach(self):
        self._had_driver = False
        self._dev = usb.core.find(idVendor=0x0001, idProduct=0x0000)
        if self._dev is None:
            raise ValueError("Device not found")

        if self._dev.is_kernel_driver_active(0):
            self._dev.detach_kernel_driver(0)
            self._had_driver = True

        self._dev.set_configuration()

    def release(self):
        usb.util.release_interface(self._dev, 0)
        if self._had_driver:
            self._dev.attach_kernel_driver(0)

    def battery_status(self):
        while True:
            try:
                self.attach()
            except:
                print sys.exc_info()
            try:
                ret = usb.util.get_string(self._dev, 0x03, langid=0x0409)
                if ret[0] == "(" and ret[38] == "0":
                    self.online = True
                    print "online"
                else:
                    self.online = False
                    print "offline"
            except:
                print sys.exc_info()
            try:
                self.release()
            except:
                print sys.exc_info()
            time.sleep(0.5)

a = ups()
a.battery_status()
