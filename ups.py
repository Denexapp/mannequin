"""
by Denexapp

"""

import threading
import subprocess
import denexapp_config as dconfig
import time

class ups():

    def __init__(self, gsm_object):
        self.warning_sent = False
        self.ready_to_work = True
        self.stop = False
        self.gsm_object = gsm_object

    def start_monitoring(self):
        thread = threading.Thread(target=self.__start_monitoring_action)
        thread.daemon = True
        thread.start()

    def stop_monitoring(self):
        self.stop = True

    def __start_monitoring_action(self):
        self.stop = False
        time.sleep(12)
        while True:
            status = subprocess.check_output("upsc dexp@localhost | grep ups.status", shell=True)[11:]
            if (status.find(" OB") != -1) or (status.find(" LB") != -1):
                if not self.warning_sent:
                    self.gsm_object.send_no_power()
                    self.ready_to_work = False
                    self.warning_sent = True
            elif status.find(" OL") != -1:
                if self.warning_sent is True:
                    self.gsm_object.send_power_on()
                    self.ready_to_work = True
                    self.warning_sent = False
            time.sleep(dconfig.check_interval/1000)
            if self.stop:
                break

    def able_to_work(self):
        return self.ready_to_work
