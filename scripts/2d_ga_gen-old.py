#!/usr/bin/env python3
# 2D Ghost Atom Generator (OLD)
# 2d_ga_gen.py
# Generates 2D array of Bq atoms for Gaussian input files
# Author: Dylan Morgan

import numpy
import argparse


class InputGenerator:

    def __init__(self):
        self.bq_coors = []

    def cli_cmds(self):
        parser = argparse.ArgumentParser(description='Generates Bq atoms for Gaussian input files in 2D')
        parser.add_argument('originalfile', help='original file to copy')
        parser.add_argument('newfile', help='new file to write to')
        parser.add_argument('-v', '--verbose',  # Is it possible to pipe this to less?
                            action='store_true',
                            help='print output of Bq coordinates to append to file')

        plane = parser.add_mutually_exclusive_group(required=True)

        plane.add_argument('-xy', '--xy_plane',
                           action='store_true',
                           help='specify the coordinate plane as the xy plane')
        plane.add_argument('-xz', '--xz_plane',
                           action='store_true',
                           help='specify the coordinate plane as the xz plane')
        plane.add_argument('-yz', '--yz_plane',
                           action='store_true',
                           help='specify the coordinate plane as the yz plane')

        self.args = parser.parse_args()

    def gen_bq_coors(self):
        try:
            coor = input('\nEnter coordinates (x, y, z) for first ghost atom separated by spaces: ')
            vs = input('Specify vector spacings (x, y, z) separated by spaces: ')
            bq_no = int(input('Specify number of ghost atoms (in 1 dimension): '))

            n0 = numpy.array(coor.split(), float)
            delta_xyz = numpy.array(vs.split(), float)

            if self.args.xy_plane is True:
                for n1 in range(bq_no):
                    xn = n0 + n1 * delta_xyz

                    for n2 in range(bq_no):
                        yn = n0 + n2 * delta_xyz
                        self.bq_coors.append(f'Bq {xn[0]} {yn[1]} {xn[2]}')  # Adds each coor as new line in new file

            elif self.args.xz_plane or self.args.yz_plane is True:  # Crude fix. Will aim to improve before 1st release
                for n1 in range(bq_no):
                    xn = n0 + n1 * delta_xyz

                    for n2 in range(bq_no):
                        yn = n0 + n2 * delta_xyz
                        self.bq_coors.append(f'Bq {xn[0]} {xn[1]} {yn[2]}')

            if self.args.verbose is True:
                print('\nOutput:\n')  # Shows usr list of coors generated
                print(*self.bq_coors, sep='\n')  # Is there a way to pipe this to less instead? eg. print... | less

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
                    print(f'\nContents of file:\n\n{contents}')

        print('Task completed successfully!')


if __name__ == '__main__':
    ig = InputGenerator()
    ig.cli_cmds()
    ig.gen_bq_coors()
    ig.check()
    ig.copy_inp()
