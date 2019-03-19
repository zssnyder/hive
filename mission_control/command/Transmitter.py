import threading

#class Transmitter:
    #def __init__():

    #def Transmit():

    #def CreateRecieveThread():

class Reciever(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("reciever creating")

    def run(self):
        print("reciever starting")


reciever = Reciever()
reciever.start()