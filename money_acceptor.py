import serial
import threading
import denexapp_config as dconfig

class money_acceptor():
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
    0x2F: "Enable acceptor response",
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
        self.accept_money = False
        self.ser = serial.Serial(dconfig.money_device, 9600)

    def send(self,command):
        print "->", command
        self.ser.write(chr(self.commands[command]))

    def read(self):
        message = ord(self.ser.read())
        print "<-", message
        return message

    def start_working(self):
        self.thread = threading.Thread(target=self.__start_working_action())
        self.thread.daemon = True
        self.thread.start()

    def accept_money(self):
        self.accept_money = True

    def reject_money(self):
        self.accept_money = False

    def __start_working_action(self):
        while True:
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
                if response == bytearray(self.reverse_replies["[Bill byte]"]):
                    print "Got money"
                    after_bill_byte = self.read()
                    if self.accept_money:
                        if after_bill_byte == replies
                        self.send("accept")
                    else:
                        self.send("reject")

                     print "Accept sent"
