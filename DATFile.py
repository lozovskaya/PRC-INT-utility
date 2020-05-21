class DAT:
    def __init__(self, inputDAT):
        self.windows = -1
        self.regime = -1
        self.parameters = dict()
        if (type(inputDAT) == list):
            self.DAT_file = inputDAT
        elif (type(inputDAT) == str):
            self.DAT_file = inputDAT.split('\n')
        else:
            raise ValueError("Некорретный DAT-файл")

    def __str__(self):
        return ', '.join('{}: {}'.format(key, value) for key, value in self.__dict__.items() if key != 'DAT_file')


    def index(self, substring):
        for i in range(len(self.DAT_file)):
            if (substring in self.DAT_file[i]):
                return i
        raise ValueError("Некорретный DAT-файл")


    def count_windows(self):  # возвращает общее число независимых окон, -1 если файл некорректный
        if (self.windows != -1):
            return self.windows
        begin = "#VAR"
        DAT_string = self.DAT_file[self.index(begin)]
        DAT_string = DAT_string.split()[1]
        number = 0
        for i in range(len(DAT_string)):
            if (DAT_string[i].isdigit()):
                number *= 10
                number += int(DAT_string[i])
            else:
                break
        assert  (number >= 0)
        self.windows = number
        return self.windows


    def mode_MTMB(self):  # какой МТ/МВ оператор вычисляет программа PRC_MRR и по какой методике
        if (self.regime != -1):
            return self.regime
        begin = "#SEL"
        DAT_string = self.DAT_file[self.index(begin)]
        DAT_string = DAT_string.split()
        self.regime = DAT_string[3]
        return self.regime


    def get_param(self):
        begin = "#SEL"
        cnt = 0
        index = 0
        for i in range(len(self.DAT_file)):
            if (begin in self.DAT_file[i]):
                cnt += 1
            if (cnt == 3):
                index = i
                break
        for i in range(index, len(self.DAT_file)):
            if (begin in self.DAT_file[i]):
                string = self.DAT_file[i].split()
                self.parameters[string[1]] = [string[4], string[5], string[8], 
                                              string[9], string[12], string[13]]
            else:
                break


    def init(self):
        count_windows();
        mode_MTMB()
        get_param()


regime_name = {"00" : "Zss", "22" : "Zrr", "10" : "Wss", "52" : "Wrr", "32" : "M"}

def parse_DAT(path):
    with open(path, 'r') as f:
        DATf = DAT(f.readlines()).init()
    return DATf

if (__name__ == '__main__'):  # для отладки
    with open("bVS0_ALX.DAT", "r") as f:
        DATf = DAT(f.readlines())
    print(DATf.count_windows())
    print(DATf.mode_MTMB())
    DATf.get_param()

