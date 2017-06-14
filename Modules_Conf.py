class Module:
    def __init__(self, Type = "", In_Channel_Count = 0, Out_Channel_Count = 0):
        self.Module_State = False
        self.Type = Type
        self.In_Channel_Count = In_Channel_Count
        self.Out_Channel_Count = Out_Channel_Count
        if self.Type == "AI":
            self.InField = [0 for i in range(self.In_Channel_Count)]
        elif self.Type == "DI":
            self.InField = [False for i in range(self.In_Channel_Count)]
        elif self.Type == "AO":
            self.OutField = [0 for i in range(self.Out_Channel_Count)]
        elif self.Type == "DO":
            self.OutField = [False for i in range(self.Out_Channel_Count)]
        elif self.Type == "AI/AO":
            self.InField = [0 for i in range(self.In_Channel_Count)]
            self.OutField = [0 for i in range(self.Out_Channel_Count)]
        elif self.Type == "DI/DO":
            self.InField = [False for i in range(self.In_Channel_Count)]
            self.OutField = [False for i in range(self.Out_Channel_Count)]

# -------------------------------------------------------------------------------------------
DM72F0 = Module(Type="DI/DO",In_Channel_Count=7, Out_Channel_Count=2)
DM72F1 = Module(Type="DI/DO",In_Channel_Count=7, Out_Channel_Count=2)
A3 = Module(Type="DI",In_Channel_Count=12)
A4 = Module(Type="DI",In_Channel_Count=12)
A5 = Module(Type="DO",Out_Channel_Count=12)
A6 = Module(Type="DO",Out_Channel_Count=12)
A7 = Module(Type="AI",In_Channel_Count=4)
A8 = Module(Type="AI",In_Channel_Count=4)
A9 = Module(Type="AI",In_Channel_Count=4)
A10 = Module(Type="AI",In_Channel_Count=4)
A11 = Module(Type="AO",Out_Channel_Count=4)
# -------------------------------------------------------------------------------------------

