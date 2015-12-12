import money_acceptor
import time

money_acceptor_object = money_acceptor.money_acceptor()
money_acceptor_object.start()
money_acceptor_object.accept_money()
while True:
    time.sleep(10)
