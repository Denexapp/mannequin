import time
import sys

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



a = ups()
a.battery_status()
