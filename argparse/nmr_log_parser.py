#!usr/bin/env python3
# nmr_log_parser.py
# Parses information from Gaussian output file to a new file
# Author: Dylan Morgan


class LogParser:

    '''
Parses Bq coors, isotropic values, and tensors from Gaussian output (.log) file to new file.

REQUIRED: output (.log) AND input (.com) files

    '''

# automate in future so this doesn't need to be done manually

    def __init__(self):  # defines variables/lists for later functions
        self.inp_filename = None
        self.out_filename = None
        self.coors = []
        self.iso_values = []
        self.tensors = []

    def read_coors(self):
        self.inp_filename = input('Gaussian input file name: ')

        with open(self.inp_filename) as comfile:
            for line in comfile:
                if 'Bq' in line:
                    self.coors.append(line)  # appends coors of ghost atoms from input file

    def read_iso_values(self):
        self.out_filename = input('Gaussian output file name: ')
        logline = []  # only needed for this function

        with open(self.out_filename) as logfile:
            for line in logfile:
                if 'Isotropic' in line and 'Bq' in line:  # only appends isotropic values of ghost atoms
                    logline.append(line.split())

            for line in logline:
                for word in line:
                    if word == line[4]:  # 5th space separated string in line is desired isotropic value
                        self.iso_values.append(float(word))

    def read_tensors(self):
        with open(self.out_filename) as logfile:
            while True:
                try:
                    line = next(logfile)
                    if 'Isotropic' in line and 'Bq' in line:
                        line = next(logfile)
                        self.tensors.append(line)
                        line = next(logfile)
                        self.tensors.append(line)
                        line = next(logfile)
                        self.tensors.append(line)  # appends next 3 lines after line containing 'Isotropic' and 'Bq'

                except StopIteration:
                    break

        print(f'\nFinished parsing file: {self.out_filename}\n')

    def copy_iso_values(self):
        copy_out_filename = 'parsed_log_data'

        with open(copy_out_filename, 'w+') as copy:
            copy.write('\nGhost Atom Coordinates:\n')
            for count, line in enumerate(self.coors, 1):  # numerically specifies Bq atom
                copy.write(str(f'{count} c{line}'))  # labels coors as 'c'

            copy.write('\n\nNICS Isotropic Values:\n')
            for count, line in enumerate(self.iso_values, 1):
                copy.write(str(f'{count}  iBq:  {line}\n'))  # labels isotropic values as 'i'

            copy.write('\nGhost Atom Tensors:\n')
            for line in self.tensors:
                if 'XZ' in line:
                    copy.write(f'{line}\n')
                else:
                    copy.write(line)

        with open(copy_out_filename, 'r') as copy:
            contents = copy.read()
            print(contents)


if __name__ == '__main__':
    lp = LogParser()
    print(lp.__doc__)
    lp.read_coors()
    lp.read_iso_values()
    lp.read_tensors()
    lp.copy_iso_values()
