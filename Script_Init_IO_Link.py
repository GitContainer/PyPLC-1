from Discrete import DiscreteDB, DiscreteConvDB


# Fire In
def init_io_link():
    DiscreteConvDB[10].Device_Index = 10
    DiscreteConvDB[10].Signal_Type  = 21
    DiscreteConvDB[10].Module = 1
    DiscreteConvDB[10].Channel = 1
    DiscreteConvDB[10].InOut = False
