class IoLink:
    def __init__(self):
        self.Channel = 0        # Номер канала
        self.Module = 0         # Номер модуля IO или индекс цифрового драйвера
        self.InOut = False      # Направление сигнала (0 - вход, 1 - выход)