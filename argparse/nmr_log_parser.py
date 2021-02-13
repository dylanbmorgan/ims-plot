#!usr/bin/env python3
# nmr_log_parser.py
# Parses information from Gaussian output file to a new file
# Author: Dylan Morgan

import argparse


class LogParser:

    def __init__(self):
        self.coors = []
        self.iso_values = []
        self.tensors = []

    def cli_cmds(self):
        self.parser = argparse.ArgumentParser(description='Parses information from Gaussian output file to a new file')
        self.parser.add_argument('inpfile', help='file name of input (.com) Gaussian file')
        self.parser.add_argument('outfile', help='file name of output (.log) Gaussian file')
        self.parser.add_argument('-v', '--verbose',  # Is it possible to pipe this to less?
                                 action='store_true',
                                 help='print output of file containing parsed data')
        self.parser.add_argument('-w', '--writename',
                                 action='store_true',
                                 default='parsed_log_data.txt',
                                 help='file name to write parsed data file as')
        self.args = self.parser.parse_args()

    def read_coors(self):
        with open(self.args.inpfile) as comfile:
            for line in comfile:
                if 'Bq' in line:
                    self.coors.append(line)  # Appends coors of ghost atoms from input file

    def read_iso_values(self):
        logline = []

        with open(self.args.outfile) as logfile:
            for line in logfile:
                if 'Isotropic' in line and 'Bq' in line:  # Only appends isotropic values of ghost atoms
                    logline.append(line.split())

            for line in logline:
                for word in line:
                    if word == line[4]:  # 5th space separated string in line is desired isotropic value
                        self.iso_values.append(float(word))

    def read_tensors(self):
        with open(self.args.outfile) as logfile:
            while True:
                try:
                    line = next(logfile)
                    if 'Isotropic' in line and 'Bq' in line:
                        line = next(logfile)
                        self.tensors.append(line)
                        line = next(logfile)
                        self.tensors.append(line)
                        line = next(logfile)
                        self.tensors.append(line)
                        # Appends next 3 lines after line containing 'Isotropic' and 'Bq'
                        # These are the shielding tensors

                except StopIteration:
                    break

    def copy_iso_values(self):
        with open(self.args.writename, 'w+') as copy:
            copy.write('\nGhost Atom Coordinates:\n')
            for count, line in enumerate(self.coors, 1):  # Numerically specifies Bq atom
                copy.write(str(f'{count}  cBq: {line}'))  # Labels coors as 'c'

            copy.write('\nNICS Isotropic Values:\n')
            for count, line in enumerate(self.iso_values, 1):
                copy.write(str(f'{count}  iBq:  {line}\n'))  # Labels isotropic values as 'i'

            copy.write('\nGhost Atom Tensors:\n')
            for line in self.tensors:
                if 'XZ' in line:
                    copy.write(f'{line}\n')
                else:
                    copy.write(line)

        if self.args.verbose is True:
            with open(self.args.writename, 'r') as copy:
                contents = copy.read()
                print(contents)

        print(f'\nFinished parsing files: {self.args.inpfile} & {self.args.outfile}')


if __name__ == '__main__':
    lp = LogParser()
    lp.cli_cmds()
    lp.read_coors()
    lp.read_iso_values()
    lp.read_tensors()
    lp.copy_iso_values()
