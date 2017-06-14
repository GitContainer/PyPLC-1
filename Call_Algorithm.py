from DiscreteConv_Work import discreteconvwork
from Script_Init_IO_Link import init_io_link
import time

def call_algorithms():
    time_before = time.time()
    init_io_link()
    discreteconvwork()
    cycle_time = time.time() - time_before
    #print("cycle_time = ", cycle_time)
