import threading
import time

class PrintNumberThreads(threading.Thread):
    def run(self):
        for i in range(5) :
            print(f"Numéro : {i}")
            time.sleep(1)        

#Création d'un thread
thread = PrintNumberThreads()
thread.start()


for i in range(5) :
    print(f"Thread principal : {i}")
    time.sleep(1)



from Cabine.Factory import Factory
Factory.Son

