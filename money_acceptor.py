import time
import serial
import threading
import denexapp_config as dconfig

class money_acceptor(threading.Thread):
    # this wasn't the best idea to use 4 globals here
    # but it should work fine anyway
    global cash_inside
    global cash_session
    global cash_banknotes
    global cash_last_pay_time

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
        0x5E: "Disable acceptor response",}

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

        try:
            money_file = open("cash_inside_file")
        except:
            money_file = open("cash_inside_file","w")
            money_file.write("0")
            money_file.close()
            money_file = open("cash_inside_file")
        self.cash_inside = int(money_file.read())
        money_file.close()

        try:
            money_file = open("cash_banknotes_file")
        except:
            money_file = open("cash_banknotes_file","w")
            money_file.write("0")
            money_file.close()
            money_file = open("cash_banknotes_file")
        self.cash_banknotes = int(money_file.read())
        money_file.close()

        self.accept_money_var = False
        print "Init: self.accept_money_var = False"
        self.ser = serial.Serial(dconfig.money_device, 9600)

    def send(self,command):
        print "->", command
        self.ser.write(chr(self.commands[command]))

    def read(self):
        message = ord(self.ser.read())
        if message in self.replies.keys():
            print "<-", message, self.replies[message]
        else:
            print "<-", message
        return message

    def add_cash(self,value):
        self.cash_inside += value
        self.cash_banknotes += 1
        self.cash_session += value
        self.cash_last_pay_time = time.time()
        money_file = open("cash_inside_file","w")
        money_file.write(str(self.cash_inside))
        money_file.close()
        money_file = open("cash_banknotes_file","w")
        money_file.write(str(self.cash_banknotes))
        money_file.close()

    def start_working(self):
        # self.thread = threading.Thread(target=self.__start_working_action())
        # self.thread.daemon = True
        # self.thread.start()
        self.__start_working_action()
        print "start_working finished"

    def accept_money(self):
        self.accept_money_var = True
        print "accept_money: self.accept_money_var = True"

    def reject_money(self):
        self.accept_money_var = False

    def run(self):
        self.__start_working_action()

    def __start_working_action(self):
        print "Money acceptor working thread started"
        while True:
            time.sleep(0.01)
            if self.ser.inWaiting():
                response = self.read()

                # init
                if response == self.reverse_replies["Power supply on / Bill verified"]:
                    self.send("accept")
                    self.send("enable")

                # disable inhibit mode
                if response == self.reverse_replies["Communication failed"]:
                    self.send("accept")

                #accept a bill
                if response == self.reverse_replies["[Bill byte]"]:
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
                            pass
                            #self.send("get_status")
                    else:
                        print "accept_money_var is ", self.accept_money_var
                        #self.send("reject")
                # if response == self.reverse_replies["Exception has been recovered"]:
                #     self.send("enable")
                if response == 254:
                    self.send("get_status")