from collections import defaultdict

class INF:
    def __init__(self, inputINF, index=0):
        self.win_number = -1
        i = index
        while ("WINDOW" not in inputINF[i] or "NUMBER" not in inputINF[i]):
            i += 1
        self.index = i
        self.number_of_extents = -1
        self.selected_extents = -1
        self.parameters = defaultdict(dict)
        self.plain_table = []
        if (type(inputINF) == list):
            self.INF_file = inputINF
        elif (type(inputINF) == str):
            self.INF_file = inputINF.split('\n')
        else:
            raise ValueError("Некорретный INF-файл")


    def __str__(self):
        return ', '.join('{}: {}'.format(key, value) for key, value in self.__dict__.items() if key != 'INF_file')


    def get_number_window(self):
        for i in range(self.index, len(self.INF_file)):
            a = self.INF_file[i].split()
            if ("WINDOW" in a and "NUMBER" in a):
                self.win_number = a[-1]
                break;


    def get_parameters(self):
        i = self.index
        while (i < len(self.INF_file) and not "STATISTICS" in self.INF_file[i]):
            i += 1
        names = self.INF_file[i].split()
        del names[1]
        self.plain_table.append(names)
        names = names[1:]
        i += 1
        for j in range(7):
            if (j == 6):
                continue
            ind = i + j
            row = self.INF_file[ind].split()
            num0 = row[0]
            row = row[2:]
            self.plain_table.append(row);
            self.plain_table[-1].insert(0, num0)
            for k in range(len(names)):
                self.parameters[num0][names[k]] = row[k]


    def get_numberofextents(self):
        for i in range(self.index, len(self.INF_file)):
            a = self.INF_file[i].split()
            if ("NUMBER" in a and "EXTENTS" in a):
                self.number_of_extents = a[-1]
                break;


    def get_selectedextents(self):
        for i in range(self.index, len(self.INF_file)):
            a = self.INF_file[i].split()
            if ("SELECTED" in a and "EXTENTS" in a):
                self.selected_extents = a[-1]
                break;
    

    def end_of_window(self):
        i = self.index + 1
        while i < len(self.INF_file) and ("WINDOW" not in self.INF_file[i] or "NUMBER" not in self.INF_file[i]):
            i += 1
        return i


    def init(self):
        self.get_number_window();
        self.get_parameters();
        self.get_numberofextents();
        self.get_selectedextents();
        return self.end_of_window()


def parse_INF(path):
    with open(path, 'r') as f:
        INF_input = f.readlines()
    index = 0
    INFwindows = []
    while (index < len(INF_input)):
        new_element = INF(INF_input, index)
        new_element.init()
        INFwindows.append(new_element)
        index = new_element.end_of_window()
    return INFwindows


if (__name__ == '__main__'):
    with open("bVS0_Aa1.inf", 'r') as f:
        INFf = f.readlines();
    INFf = INF(INFf)
    INFf.init()
    for i in INFf.parameters:
        print(i)
