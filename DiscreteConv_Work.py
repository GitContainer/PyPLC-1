from Discrete import *
from Script_IO_Discrete import script_io_discrete_fb

geterror = 0
setvalue = 1
getvalue = 2


def discreteconvwork():
    # Обработка ФБ
    for i in range(10, DiscreteConv_DB_UBound):

        if DiscreteConvDB[i].Signal_Type == 0:
            continue
        # Считывание сигнала
        if DiscreteConvDB[i].InOut:
            # Выходной сигнал - считывание значение с устройства
            if DiscreteConvDB[i].Signal_Type == 22:
                DiscreteConvDB[i].Input = DiscreteDB[DiscreteConvDB[i].Device_Index].State
                DiscreteDB[DiscreteConvDB[i].Device_Index].Emul_State = (
                    DiscreteDB[DiscreteConvDB[i].Device_Index].Emul_State or DiscreteConvDB[i].Emul_Switch)
                DiscreteDB[DiscreteConvDB[i].Device_Index].Signal_Error = (
                    DiscreteDB[DiscreteConvDB[i].Device_Index].Signal_Error or DiscreteConvDB[i].Signal_Error)
        else:
            # Входной сигнал - считывание значение с входа

            DiscreteConvDB[i].Input = script_io_discrete_fb(gettype=getvalue, module=DiscreteConvDB[i].Module,
                                            channel=DiscreteConvDB[i].Channel, value=DiscreteConvDB[i].Input)
# -------------------------------------------------------------------------------------------
    # Вызов функционального блока
        DiscreteConvDB[i].work()
# -------------------------------------------------------------------------------------------
        # Запись сигнала
        if DiscreteConvDB[i].InOut:
            # Выходной сигнал - запись в выход
            script_io_discrete_fb(gettype=setvalue, module=DiscreteConvDB[i].Module,
                                  channel=DiscreteConvDB[i].Channel, value=DiscreteConvDB[i].Output)
        else:
            if DiscreteConvDB[i].Signal_Type == 21:
                DiscreteDB[DiscreteConvDB[i].Device_Index].State = DiscreteConvDB[i].Output
                DiscreteDB[DiscreteConvDB[i].Device_Index].Emul_State = (
                    DiscreteDB[DiscreteConvDB[i].Device_Index].Emul_State or DiscreteConvDB[i].Emul_Switch)
                DiscreteDB[DiscreteConvDB[i].Device_Index].Signal_Error = (
                    DiscreteDB[DiscreteConvDB[i].Device_Index].Signal_Error or DiscreteConvDB[i].Signal_Error)