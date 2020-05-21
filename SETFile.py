class SET:
    def __init__(self, inputSET, index=0):
        self.mode = inputSET[index]
        self.index = index + 1
        self.SET_file = inputSET
        self.parameters = dict()
        if (index == 0):
            for i in range(len(self.SET_file)):
                if (type(self.SET_file[i]) == str):
                    self.SET_file[i] = self.SET_file[i].split()


    def to_end_the_mode(self):
        i = self.index + 1
        while (i < len(self.SET_file) and len(self.SET_file[i]) != 1):
            i += 1
        return i


    def parse_by_mode(self): # нумерация с 1, нулевой элемент - пустой
        names = self.SET_file[self.index][1:]
        for name in names:
            self.parameters[name] = [-1]
        names.insert(0, -1)
        for i in range(self.index + 1, self.to_end_the_mode()):
            for j in range(1, len(self.SET_file[i])):
                self.parameters[names[j]].append(self.SET_file[i][j])
        

def parse_SET(path):
    with open(path, "r") as f:
        SET_input = f.readlines()
    SETmodes = []
    index = 0
    while (index < len(SET_input)):
        new_element = SET(SET_input, index)
        new_element.parse_by_mode()
        SETmodes.append(new_element)
        index = new_element.to_end_the_mode()
    return SETmodes


if (__name__ == '__main__'):
    with open("settings_ts6_1.set", "r") as f:
        SETf = f.readlines()
    parse_SET(SETf)
    SETf = SET(SETf)
    SETf.parse_by_mode()
    for i in SETf.parameters:
        print(i, SETf.parameters[i])
