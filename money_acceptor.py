import time
import serial
import threading
import file_io
import denexapp_config as dconfig
import math

class money_acceptor(threading.Thread):

    replies = {
        0x80: "[Device start byte]",
        0x8f: "Power supply on / Bill verified",
        0x26: "Communication failed",
        0x81: "[Bill byte]",
        0x40: "Bill value 1",
        0x41: "Bill value 2",
        0x42: "Bill value 3",
        0x43: "Bill value 4",
        0x44: "Bill value 5",
        0x10: "Stacked (Bill accept finished)",
        0x11: "Bill accept failed",
        0x20: "Motor failure",
        0x21: "Checksum error",
        0x22: "Bill jam",
        0x23: "Bill remove",
        0x24: "Stacker open",
        0x25: "Sensor problem",
        0x27: "Bill fish",
        0x28: "Stacker problem",
        0x29: "Bill reject",
        0x2A: "Invalid command",
        0x2E: "Reserved",
        0x2F: "Exception has been recovered",
        0x5E: "Disable acceptor response"}

    reverse_replies = {}
    for i, k in replies.items():
        reverse_replies[k] = i

    commands = {
        "accept": 0x02,
        "reject": 0x0f,
        "escrow_holdt": 0x18,
        "enable": 0x3e,
        "disable": 0x5e,
        "get_status": 0x0c,
        "reset": 0x30,
    }

    def __init__(self):
        threading.Thread.__init__(self)
        self.cash_last_pay_time = time.time()
        self.cash_inside = file_io.read("cash_inside_file")
        self.cash_banknotes = file_io.read("cash_banknotes_file")
        self.capacity = file_io.read("cash_capacity_file")
        if self.capacity == 0:
            self.set_capacity(dconfig.money_capacity_default)
        self.price = file_io.read("cash_price_file")
        if self.price == 0:
            self.set_price(dconfig.payment_price_default)
        self.cash_session = 0
        self.accept_money_var = False
        self.money_send_warning = False
        self.ser = serial.Serial(dconfig.money_device, 9600)

    def able_to_work(self):
        return self.cash_banknotes <= (self.capacity - math.ceil(self.price/10))

    def set_capacity(self, capacity):
        self.capacity = capacity
        file_io.write("cash_capacity_file", capacity)

    def set_price(self, price):
        self.price = price
        file_io.write("cash_price_file", price)

    def reset(self):
        self.cash_inside = 0
        self.cash_banknotes = 0
        file_io.write("cash_inside_file", self.cash_inside)
        file_io.write("cash_banknotes_file", self.cash_banknotes)
        self.money_send_warning = False

    def banknotes_inside(self):
        return self.cash_banknotes

    def money_inside(self):
        return self.cash_inside

    def send(self, command):
        print "money ->", command
        self.ser.write(chr(self.commands[command]))

    def read(self):
        message = ord(self.ser.read())
        if message in self.replies.keys():
            print "money <-", message, self.replies[message]
        else:
            print "money <-", message
        return message

    def add_cash(self, value):
        self.cash_inside += value
        self.cash_banknotes += 1
        self.cash_session += value
        self.cash_last_pay_time = time.time()
        file_io.write("cash_inside_file", self.cash_inside)
        file_io.write("cash_banknotes_file", self.cash_banknotes)

    def accept_money(self):
        self.accept_money_var = True

    def reject_money(self):
        self.accept_money_var = False

    def run(self):
        self.__start_working_action()

    def __start_working_action(self):
        self.send("accept")
        print self.ser.name
        while True:
            time.sleep(0.01)
            if self.ser.inWaiting():
                print "ser.inWaiting"
                response = self.read()

                # init
                if response == self.reverse_replies["Power supply on / Bill verified"]:
                    self.send("accept")

                # disable inhibit mode
                if response == self.reverse_replies["Communication failed"]:
                    self.send("accept")

                #accept a bill
                if response == self.reverse_replies["[Bill byte]"]:
                    after_bill_byte = self.read()
                    if after_bill_byte == self.reverse_replies["Power supply on / Bill verified"]:
                        after_bill_byte = self.read()
                    if self.accept_money_var:
                        if after_bill_byte == self.reverse_replies["Bill value 1"]:
                            self.send("accept")
                            self.add_cash(10)
                        elif after_bill_byte == self.reverse_replies["Bill value 2"]:
                            self.send("accept")
                            self.add_cash(50)
                        elif after_bill_byte == self.reverse_replies["Bill value 3"]:
                            self.send("accept")
                            self.add_cash(100)
                        else:
                            self.send("reject")
                    else:
                        self.send("reject")
