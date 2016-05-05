"""
by Denexapp

"""

import threading
import usb.core
import usb.util
import denexapp_config as dconfig
import time
import sys

class ups():
    def __init__(self, gsm_object):
        self.warning_sent = False
        self.ready_to_work = True
        self.stop = False
        self.gsm_object = gsm_object
        self.online = True

    def start_monitoring(self):
        thread = threading.Thread(target=self.__start_monitoring_action)
        thread.daemon = True
        thread.start()

    def stop_monitoring(self):
        self.stop = True

    def __start_monitoring_action(self):
        self.stop = False
        time.sleep(13)
        print "started_monitor"
        while True:
            self.battery_status_update()
            # print "Warning sent ==", self.warning_sent, "self.online ==", self.online
            if self.online is False:
                if self.warning_sent is False:
                    print "sms sending started"
                    self.gsm_object.send_no_power()
                    self.ready_to_work = False
                    self.warning_sent = True
                    print "sms sent"
            else:
                if self.warning_sent is True:
                    print "sms sending started"
                    self.gsm_object.send_power_on()
                    self.ready_to_work = True
                    self.warning_sent = False
                    print "sms sent"
            time.sleep(dconfig.check_interval/1000)
            if self.stop:
                break

    def able_to_work(self):
        return self.ready_to_work

    def attach(self):
        self._had_driver = False
        self._dev = usb.core.find(idVendor=dconfig.vendor_id, idProduct=dconfig.product_id)
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

    def battery_status_update(self):
        try:
            self.attach()
        except:
            print sys.exc_info()
        try:
            ret = usb.util.get_string(self._dev, 0x03, langid=0x0409)
            # print ret
            if ret[0] == "(":
                if ret[38] == "0":
                    self.online = True
                    # print "online"
                elif ret[38] == "1":
                    self.online = False
                    # print "offline"
        except:
            print sys.exc_info()
        try:
            self.release()
        except:
            print sys.exc_info()
        time.sleep(0.5)
