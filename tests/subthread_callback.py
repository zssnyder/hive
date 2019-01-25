
import thread

def loop(callback):
    for i in range(10):
        thread.start_new_thread(callback, ("I'm running " + str(i),))

class TestClass():

    def callback(self, text):
        print(text)

    def run(self):
        thread.start_new_thread(loop, (self.callback, ))
        print("Run finished")

if __name__ == "__main__":
    
    test = TestClass()
    test.run()

    print("Program finished")

    while 1: pass