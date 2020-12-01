
# Purely for somewhere to play with code where I can't accidentally mess everthing up


def read_coors(self):
    with open(self.filename) as logfile:
        for line in logfile:
            self.all_lines.append(line)

    for line in self.all_lines:
        if 'Isotropic' in line and 'Bq' in line:
            self.coors.append(line[1]) 
            self.coors.append(line[2])
            self.coors.append(line[3])

            #trying to select the line after the line which contains the strings 'Isotropic' and 'Bq'



class log_parser:

    def __init__(self):
        self.filename = None
        self.iso_values = []
        self.all_lines = []
        self.coors = []

    def read_coors(self):
        with open(self.filename) as logfile:
            while True:
                try:
                    line = next(logfile)
                except StopIteration:
                    print(f'Finished parsing file {self.filename}')
                    break

                if 'Isotropic' and 'Bq' in line:
                    line = next(logfile)
                    self.coors.append(line)

        print(*self.coors, sep = '\n')
