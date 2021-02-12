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
        self.parser = argparse.ArgumentParser(description='Generates Bq atoms for Gaussian input files')
        self.parser.add_argument('originalfile', help='Original file to copy')
        self.parser.add_argument('newfile', help='New file to write to')
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
            deltaz = numpy.array([0, 0, deltaxyz[2]])  # generates coors for file

            for xn in range(bq_no):
                nx = n0 + xn * deltax

                for yn in range(bq_no):
                    ny = n0 + yn * deltay

                    for zn in range(bq_no):
                        nz = n0 + zn * deltaz
                        self.bq_coors.append(f'Bq {nx[0]} {ny[1]} {nz[2]}')  # adds each coor as new line in new file

            print('\n')
            print('Output:\n')  # shows usr list of coors generated
            print(*self.bq_coors, sep='\n')  # is there a way to pipe this to less instead? eg. print... | less

        except (IndexError, ValueError) as error:
            print('\nThere was an error in interpreting your input:')
            print(error)
            print('\nPlease try again:')
            self.bq_coors.clear()
            self.gen_bq_coors()

    def check(self):
        cont = input('\nProceed? (y/n) ')

        if cont.lower() == 'y' or cont.lower() == 'yes':
            self.copy_inp()

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
