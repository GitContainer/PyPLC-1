from System import IoLink
from Modules_Conf import *
def script_io_discrete_fb(gettype, module, channel, value):
    """
    GetError 	:= 0,
    SetValue 	:= 1,
    GetValue	:= 2
    """

    module = module
    channel = channel
    error = True

    if gettype == 2:
        out = False
        if module == 0:
            out = value
            error = False
        elif module == 1:
            module_state = False
            if channel == 0:
                out = DM72F0.InField[channel]
            elif channel == 1:
                out = DM72F0.InField[channel]
            elif channel == 2:
                out = DM72F0.InField[channel]
            elif channel == 3:
                out = DM72F0.InField[channel]
            elif channel == 4:
                out = DM72F0.InField[channel]
            elif channel == 5:
                out = DM72F0.InField[channel]
            elif channel == 6:
                out = DM72F0.InField[channel]
    elif gettype == 1:
        if module == 1:
            module_state = False
            if channel == 0:
                DM72F0.OutField[channel] = module_state or value
            elif channel == 1:
                DM72F0.OutField[channel] = module_state or value
    return out
