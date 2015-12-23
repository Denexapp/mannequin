import time
import serial
import file_io
import threading
import denexapp_config as dconfig

class gsm(threading.Thread):

    def __init__(self, money_acceptor_object, card_dispenser_object):
        self.money_acceptor_object = money_acceptor_object
        self.card_dispenser_object = card_dispenser_object

        self.phone1 = file_io.read("gsm_phone1_file")
        if self.phone1 == 0:
            self.phone1(dconfig.gsm_phone1_default)
            file_io.write("gsm_phone1_file", self.phone1)

        self.phone2 = file_io.read("gsm_phone2_file")
        if self.phone2 == 0:
            self.phone2(dconfig.gsm_phone2_default)
            file_io.write("gsm_phone2_file", self.phone2)

        threading.Thread.__init__(self)
        self.new_ser = serial.Serial(dconfig.gsm_device, 9600)
        self.power_on()

    def send(self, command):
        command = str(command)
        print "gsm ->", command
        self.new_ser.write(command)

    def read(self):
        message = self.new_ser.read()
        message = str(message)
        print "gsm <-", message
        return message

    def run(self):
        self.__start_working_action()

    def get_number(self, stop_char):
        string = ""
        while True:
            char = self.read()
            if char == stop_char:
                break
            string = string + char
        return int(string)

    def power_on(self):
        time.sleep(5)
        self.send('z')
        while True:
            if self.new_ser.inWaiting():
                if self.read() == 'n':
                    break
            else:
                time.sleep(0.1)
        self.send_number(1, self.phone1, False)
        self.send_number(2, self.phone2, False)

    def send_number(self, n, number, sms):
        if n == 1:
            self.send('A')
        elif n == 2:
            self.send('B')
        self.send(number)
        if sms:
            if n == 1:
                self.send('w')
                self.send(number)
                self.send('x')
            elif n == 2:
                self.send('y')
                self.send(number)
                self.send('z')

    def send_status(self, state):
        if state == "cards almost out":
            self.send('q')
        elif state == "money box almost full":
            self.send('r')
        elif state == "cards out":
            self.send('s')
        elif state == "money box full":
            self.send('t')
        else:
            self.send('a')
        self.send(self.card_dispenser_object.cards_left())
        self.send('b')
        self.send(self.card_dispenser_object.capacity)
        self.send('c')
        self.send(self.money_acceptor_object.cash_banknotes)
        self.send('d')
        self.send(self.money_acceptor_object.capacity)
        self.send('e')
        self.send(self.money_acceptor_object.cash_inside)
        self.send('f')
        self.send(self.money_acceptor_object.price)
        self.send('g')

    def send_reset_cards(self):
        self.send('h')

    def send_reset_banknotes(self):
        self.send('i')

    def send_reset_all(self):
        self.send('j')

    def send_price_set(self):
        self.send('k')
        self.send(self.money_acceptor_object.price)
        self.send('l')

    def send_banknotes_limit_set(self):
        self.send('m')
        self.send(self.money_acceptor_object.capacity)
        self.send('n')

    def send_cards_limit_set(self):
        self.send('o')
        self.send(self.card_dispenser_object.capacity)
        self.send('p')

    def __start_working_action(self):
        print self.new_ser.name
        while True:
            time.sleep(0.01)
            if self.new_ser.inWaiting():
                print "ser.inWaiting"
                response = self.read()

                if response == 'a':
                    self.send_status("normal")
                elif response == 'b':
                    self.money_acceptor_object.reset()
                    self.send_reset_banknotes()
                elif response == 'c':
                    self.card_dispenser_object.reset()
                    self.send_reset_cards()
                elif response == 'd':
                    self.money_acceptor_object.set_capacity(self.get_number('e'))
                    self.money_acceptor_object.reset()
                    self.send_banknotes_limit_set()
                elif response == 'f':
                    self.card_dispenser_object.set_capacity(self.get_number('g'))
                    self.card_dispenser_object.reset()
                    self.send_reset_cards()
                elif response == 'h':
                    self.money_acceptor_object.set_price(self.get_number('i'))
                    self.send_price_set()
                elif response == 'j':
                    self.phone1 = (self.get_number('k'))
                    file_io.write("gsm_phone1_file", self.phone1)
                    self.send_number(1, self.phone1, True)
                elif response == 'l':
                    self.phone2 = (self.get_number('m'))
                    file_io.write("gsm_phone2_file", self.phone2)
                    self.send_number(2, self.phone2, True)
                else:
                    pass
