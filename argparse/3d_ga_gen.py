#!/usr/bin/env python3
# 3d_ga_gen.py
# Generates 3D array of Bq atoms for Gaussian input files
# Author: Dylan Morgan

import numpy
import argparse


class InputGenerator:

    def __init__(self):
        self.bq_coors = []

    def cli_cmds(self):
        self.parser = argparse.ArgumentParser(description='Generates Bq atoms for Gaussian input files in 3D')
        self.parser.add_argument('originalfile', help='original file to copy')
        self.parser.add_argument('newfile', help='new file to write to')
        self.parser.add_argument('-v', '--verbose',  # Is it possible to pipe this to less?
                                 action='store_true',
                                 help='print output of Bq coordinates to append to file')
        self.args = self.parser.parse_args()

    def gen_bq_coors(self):
        try:
            coor = input('\nEnter coordinates (x, y, z) for first ghost atom separated by spaces: ')
            vs = input('Specify vector spacings (x, y, z) separated by spaces: ')
            bq_no = int(input('Specify number of ghost atoms (in 1 dimension): '))

            n0 = numpy.array(coor.split(), float)
            deltaxyz = numpy.array(vs.split(), float)
            deltax = numpy.array([deltaxyz[0], 0, 0])
            deltay = numpy.array([0, deltaxyz[1], 0])
            deltaz = numpy.array([0, 0, deltaxyz[2]])  # Generates coors for file

            for xn in range(bq_no):
                nx = n0 + xn * deltax

                for yn in range(bq_no):
                    ny = n0 + yn * deltay

                    for zn in range(bq_no):
                        nz = n0 + zn * deltaz
                        self.bq_coors.append(f'Bq {nx[0]} {ny[1]} {nz[2]}')  # Adds each coor as new line in new file

            if self.args.verbose is True:
                print('\nOutput:\n')  # Shows usr list of coors generated
                print(*self.bq_coors, sep='\n')  # I:s there a way to pipe this to less instead? eg. print... | less

        except (IndexError, ValueError) as error:
            print('\nThere was an error in interpreting your input:')
            print(error)
            print('\nPlease try again:')
            self.bq_coors.clear()
            self.gen_bq_coors()

    def check(self):
        cont = input('\nProceed? (y/n) ')

        if cont.lower() == 'y' or cont.lower() == 'yes':
            pass

        elif cont.lower() == 'n' or cont.lower() == 'no':
            self.bq_coors.clear()
            self.gen_bq_coors()
            ig.check()

        else:
            print('Not a valid answer')
            ig.check()

    def copy_inp(self):
        with open(self.args.originalfile) as original:
            with open(self.args.newfile, "w+") as copy:
                for line in original:
                    copy.write(line)

                for coor in self.bq_coors:
                    copy.write(f'{coor}\n')
                    copy.write(' ')

        if self.args.verbose is True:
            with open(self.args.newfile, "r") as copy:
                if copy.mode == "r":
                    contents = copy.read()
                    print(contents)

        print('Task failed successfully!')


if __name__ == '__main__':
    ig = InputGenerator()
    ig.cli_cmds()
    ig.gen_bq_coors()
    ig.check()
    ig.copy_inp()

# TODO:
# [X] finish testing
# [X] make help section from argparse look prettier
# [] improve self-documentation
# [X] ensure check() func works properly
# [] complete same process with other scripts
