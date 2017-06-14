from Variable_List import System_Call_Interval
from System import IoLink
# -------------------------------------------------------------------------------------------


class DiscreteConvDT(IoLink):
    def __init__(self):
        super().__init__()
        self.Input = False          # Входной сигнал
        self.Output = False         # Выходной сигнал
        self.IO_Error = False       # Ошибка привязанного сигнала
        self.Signal_Error = False   # Ошибка сигнала
        self.Invert = False         # Инверсия входного сигнала
        self.Emul_Switch = False    # Включение эмуляции
        self.Emul_Value = False     # Значение устанавливаемое на входе, при эмуляции
        self.Device_Index = 0       # Индекс устройства, к которому привязан сигнал
        self.Signal_Type = 0        # Тип сигнала
        self.Filter_Time = 500        # Время фильтрации входного сигнала


class DiscreteConvFB(DiscreteConvDT):
    '''
    В данном функциональном блоке производится обработка поступающих дискретных сигналов
    с учетом выдержки времени на установку и снятие сигнала и направления работы (инверсии)
    '''
    def __init__(self):
        super().__init__()
        self.Filter_Timer = 0       # таймер фильтрации
        self.Status = False         # текущий входящий сигнал с учетом эмуляции и инвертирования

    def work(self):
        self.Status = self.Input
        # Эмуляция
        if self.Emul_Switch:
            self.Status = self.Emul_Value

        # Инвертирование входного сигнала
        if self.Invert:
            self.Status = not self.Status

        # Фильтрация входного сигнала
        if self.Status != self.Output:
            if self.Filter_Timer >= System_Call_Interval:
                self.Filter_Timer -= System_Call_Interval
            else:
                self.Output = self.Status
        if self.Status == self.Output:
            self.Filter_Timer = self.Filter_Time

        # Обработка аварии сигнала
        self.Signal_Error = self.IO_Error
        self.IO_Error = False


class DiscreteDT:
    def __init__(self):
        self.Alarm_Delay = 0            # Задержка формирования сигнализации
        self.State = False              # Входной сигнал
        self.Signal_Error = False       # Ошибка сигнала
        self.Emul_State = False         # Состояние эмуляции сигнала
        self.Alarm_Off = False          # Отключение сигнализации из алгоритма
        self.Warning_On_User = False    # Разрешение предупреждения
        self.Error_On_User = False      # Разрешение аварии
        self.Warning = False            # Предупреждение
        self.Error = False              # Авария
        self.Warning_Emul = False       # Предупреждение: Эмуляция сигнала
        self.Warning_Error = False      # Предупреждение: Авария сигнала


class DiscreteFB(DiscreteDT):
    '''
    В данном функциональном блоке производится обработка поступающих дискретных сигналов
    с учетом выдержки времени на установку и снятие сигнала и направления работы (инверсии)
    '''
    def __init__(self):
        super().__init__()
        self.Alarm_Timer = 0        # таймер сигнализации

    def work(self):
        # Сигнализация по значению
        if self.State:
            if self.Alarm_Timer >= System_Call_Interval:
                self.Alarm_Timer -= System_Call_Interval
            else:
                self.Warning = self.Warning and not(self.Alarm_Off)
                self.Error = self.Error and not(self.Alarm_Off)
        else:
            self.Warning = False
            self.Error = False
            self.Alarm_Timer = self.Alarm_Delay

        # Сигнализация по состоянию
        self.Warning_Emul = self.Emul_State
        self.Emul_State = False
        self.Warning_Error = self.Signal_Error
        self.Signal_Error = False


# -------------------------------------------------------------------------------------------
# Обработчик дискретного сигнала
DiscreteConv_DB_UBound  = 300
DiscreteConvDB = [DiscreteConvFB() for i in range(DiscreteConv_DB_UBound)]

# Сигнализация дискретного сигнала
Discrete_DB_UBound      = 300
DiscreteDB = [DiscreteFB() for i in range(Discrete_DB_UBound)]
# -------------------------------------------------------------------------------------------


