import time, threading
from Discrete import DiscreteDB
from Modules_Conf import *
from Call_Algorithm import call_algorithms
from Variable_List import System_Call_Interval

DM72F0.InField[1] = True


while True:
    time.sleep(System_Call_Interval / 1000)
    threading.Thread(target=call_algorithms).start()

    print("DiscreteDB[10].State = ", DiscreteDB[10].State)



