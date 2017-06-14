from Variable_List import System_Call_Interval
from System import IoLink
# -------------------------------------------------------------------------------------------


class AnalogConvDT(IoLink):
    def __init__(self):
        super().__init__()
        self.Device_Index = 0   # Индекс устройства, к которому привязан сигнал
        self.Signal_Type = 0    # Тип сигнала
        self.Error = 0          # Авария сигнала
        self.Emul_Switch = 0    # Активация эмуляции
        self.Emul_Value = 0     # Значение эмулирующего сигнала
        self.Signal_Value = 0   # Значение сигнала
        self.Signal_Error = 0   # Авария канала передачи сигнала
        self.SV_Filter = 0      # Фильтрация сигнала
        self.Error_Delay = 0    # Задержка перед установкой состояния ошибки
        self.Error_Status = 0   # Состояние сигнала
        self.IA_Type = 0        # Тип аналогового сигнала
        self.IA = 0             # Значение сигнала в физических величинах
        self.IA_Max = 0         # Верхний предел входного сигнала в физических величинах
        self.IA_Min = 0         # Нижний предел входного сигнала в физических величинах
        self.SV_HI = 0          # Верхний предел шкалы выходного сигнала
        self.SV_LO = 0          # Нижний предел шкалы выходного сигнала
        self.SV = 0             # Значение преобразованного сигнала
        self.SV_Not_Emul = 0    # Значение преобразованного сигнала без учёта эмуляции


class AnalogConvFB(AnalogConvDT):
    '''
	- Добавлена защита по SV_Hi = SV_Lo для AI
	- Добавлена защита по IA_Max = IA_Min, SV_Hi = SV_Lo для AO

	Состояние Error_Status
	0	- Нет привязки
	1	- Нет связи с цифровым устройством
	2	- Выше верхнего предела
	3	- Ниже нижнего предела
	4	- Обрыв линии
	5	- Некорректное задание: IA_Max = IA_Min, SV_Hi = SV_Lo
    '''
    def __init__(self):
        super().__init__()
        self.Signal_Value_Real = 0.0      #
        self.IA_Dif_Error = 0.0       #
        self.Is_IA_Signal = False  #
        self.Error_Timer = 0  # Таймер ошибки
        self.Error_Inner = False  #
        self.HH_Inner = False  #
        self.HI_Inner = False  #
        self.LO_Inner = False  #
        self.LL_Inner = False  #
        self.Channel_Value_Real = 0.0  # Значение с аналогового входа
        self.HH_Delay_Inner = 0  # Прошедшее время с аварии
        self.LL_Delay_Inner = 0  # Прошедшее время с аварии

    def work(self):
        # Сброс аварии каждый скан
        self.Error_Status = 0

        # Выходной сигнал
        if self.InOut:
            # Эмуляция
            if self.Emul_Switch:
                self.SV = self.Emul_Value

            if self.IA_Max == self.IA_Min or self.SV_HI == self.SV_LO:
                self.Signal_Error |= 0x010
            self.Error_Status = self.Signal_Error

            if not self.Signal_Error:
                # Получение токового сигнала
                self.IA = (self.SV - self.SV_LO) / (self.SV_HI - self.SV_LO) * (self.IA_Max - self.IA_Min) + self.IA_Min

                # Формирование выходного состояния
                if self.IA_Type == 0:
                    self.Signal_Value = (self.IA - 4) / 16 * 32767
                elif self.IA_Type == 1:
                    self.Signal_Value = (self.IA - 0) / 10 * 32767
            else:
                self.Signal_Value = 0
        # Входной сигнал
        else:
            # Преобразование входного сигнала на основании его типа
            self.Is_IA_Signal = False
            if self.IA_Type == 0:
                # Токовый сигнал 4-20мА
                self.IA = (self.Signal_Value / 32767) * 16 + 4
                self.Is_IA_Signal = 0.3
                self.Is_IA_Signal = True
            if self.IA_Type == 1:
                # Сигнал по напряжению 0-10В
                self.IA = (self.Signal_Value / 32767) * 10 + 0
                self.Is_IA_Signal = 0.2
                self.Is_IA_Signal = True
            if self.IA_Type == 2:
                # Сигнал REAL
                self.Signal_Value_Real = self.Signal_Value
                self.IA = self.Signal_Value_Real
            if self.IA_Type == 3:
                # Сигнал DWord
                self.IA = self.Signal_Value

            # Проверка на аварии по входному аналоговому сигналу
            if self.Is_IA_Signal:
                if self.Signal_Value == 32767 or self.IA >= self.IA_Max:
                    self.Signal_Error |= 0x02
                if self.IA <= (self.IA_Min - self.IA_Dif_Error):
                    self.Signal_Error |= 0x04
                if self.IA_Max == self.IA_Min or self.SV_HI == self.SV_LO:
                    self.Signal_Error |= 0x10

            # Задержка аварий
            if self.Signal_Error > 0:
                if self.Error_Timer >= System_Call_Interval:
                    self.Error_Timer -= System_Call_Interval
                else:
                    self.Error_Status = self.Signal_Error
            else:
                self.Error_Timer = self.Error_Delay

                # Расчёт выходного значения
                if self.Is_IA_Signal:
                    self.SV_Not_Emul = (self.SV_Not_Emul * self.SV_Filter + ((self.IA - self.IA_Min) /
                    (self.IA_Max - self.IA_Min) * (self.SV_HI - self.SV_LO) + self.SV_LO)) / (self.SV_Filter + 1)
                else:
                    self.SV_Not_Emul = (self.SV_Not_Emul * self.SV_Filter + (self.IA * self.SV_HI + self.SV_LO)) / (self.SV_Filter + 1)

            #  Эмуляция
            if self.Emul_Switch:
                self.SV = self.Emul_Value
            else:
                self.SV = self.SV_Not_Emul

        self.Error = (self.Error_Status > 0) and not self.Emul_Switch
        # Сброс аварий сигнала
        self.Signal_Error = 0


class RealDT:
    def __init__(self):
        self.SV = 0.0            # Значение
        self.Signal_Error = False  # Ошибка входного значения
        self.Emul_State = False  # Эмуляция активна
        self.Error = False  # Ошибка датчика
        self.HH = False  # Сигнализация - превышение верхней аварийной границы
        self.HI = False  # Сигнализация - превышение верхней предупредительной границы
        self.LO = False  # Сигнализация - достижение нижней предупредительной границы
        self.LL = False  # Сигнализация - достижение нижней аварийной границы
        self.H_Off = False  # Отключение сигнализации по верхней границы
        self.L_Off = False  # Отключение сигнализации по нижней границы
        self.HH_On = False  # Включение сигнализации по верхней аварийной уставке
        self.HI_On = False  # Включение сигнализации по верхней предупредительной уставке
        self.LO_On = False  # Включение сигнализации по нижней предупредительной уставке
        self.LL_On = False  # Включение сигнализации по нижней аварийной уставке
        self.HMI_State = 0  # Слово состояния для панели
        self.HMI_Units = 0  # Единицы измерения для панели
        self.HH_Value = 0.0  # Значение верхнего предела аварийной сигнализации
        self.HI_Value = 0.0  # Значение верхнего предела предупредительной сигнализации
        self.LO_Value = 0.0  # Значение нижнего предела предупредительной сигнализации
        self.LL_Value = 0.0  # Значение нижнего предела аварийной сигнализации
        self.Deadband = 0  # Гистерезис для предупредительной сигнализации
        self.HH_Delay = 0  # Задержка перед активацией аварии по верхней уставке
        self.LL_Delay = 0  # Задержка перед активацией аварии по нижней уставке


class RealFB(RealDT):
    '''
    В данном функциональном блоке производится обработка поступающих дискретных сигналов
    с учетом выдержки времени на установку и снятие сигнала и направления работы (инверсии)
    '''
    def __init__(self):
        super().__init__()
        self.HH_Inner = False        # Сигнализация по верхнему аварийному уровню
        self.HI_Inner = False  # Сигнализация по верхнему предупредительному уровню
        self.LO_Inner = False  # Сигнализация по нижнему предупредительному уровню
        self.LL_Inner = False  # Сигнализация по нижнему аварийному уровню
        self.HH_Delay_Inner = 0  # Прошедшее время с аварии
        self.LL_Delay_Inner = 0  # Прошедшее время с аварии
        self.Error_Timer = 0  # Таймер ошибки

    def work(self):
        # Сигнализация по значению
        self.Error = self.Signal_Error
        self.Signal_Error = 0

        # Сигнализация.
        # Установка предупредительных и аварийных границ.

        # Проверка и установка верхнего аварийного предела.
        if self.SV >= self.HH_Value:
            if self.HH_Delay > self.HH_Delay_Inner:
                self.HH_Delay_Inner += System_Call_Interval
            else:
                self.HH_Inner = self.HH_On
        if (self.SV < (self.HH_Value - self.Deadband)) or not self.HH_On or self.Error:
            self.HH_Inner = False
            self.HH_Delay_Inner = 0
        self.HH = self.HH_Inner and not self.H_Off

        # Проверка и установка верхнего предупредительного предела.
        if self.SV >= self.HI_Value:
            self.HI_Inner = self.HI_On
        if (self.SV < (self.HI_Value - self.Deadband)) or not self.HI_On or self.Error:
            self.HI_Inner = False
        self.HI = self.HI_Inner and not self.H_Off

        # Проверка и установка нижнего предупредительного предела.
        if self.SV <= self.LO_Value:
            self.LO_Inner = self.LO_On
        if (self.SV > (self.LO_Value + self.Deadband)) or not self.LO_On or self.Error:
            self.LO_Inner = False
        self.LO = self.LO_Inner and not self.L_Off

        # Проверка и установка нижнего аварийного предела.
        if self.SV <= self.LL_Value:
            if self.LL_Delay > self.LL_Delay_Inner:
                self.LL_Delay_Inner += System_Call_Interval
            else:
                self.LL_Inner = self.LL_On
        if (self.SV > (self.LL_Value + self.Deadband)) or not self.LL_On or self.Error:
            self.LL_Inner = False
            self.LL_Delay_Inner = 0
        self.LL = self.LL_Inner and not self.L_Off

        self.HMI_State = 0
        if self.LO:
            self.HMI_State = 1
        if self.HI:
            self.HMI_State = 2
        if self.LL:
            self.HMI_State = 3
        if self.HH:
            self.HMI_State = 4
        if self.Error:
            self.HMI_State = 5
        if self.Emul_State:
            self.HMI_State += 6

# -------------------------------------------------------------------------------------------
# Обработчик аналогового сигнала
AnalogConv_DB_UBound = 100
DiscreteConvDB = [AnalogConvFB() for i in range(AnalogConv_DB_UBound)]

Real_DB_UBound = 100
DiscreteDB = [RealFB() for i in range(Real_DB_UBound)]
# -------------------------------------------------------------------------------------------













