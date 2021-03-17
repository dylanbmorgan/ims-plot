#!/usr/bin/env python3
# 2D Ghost Atom Generator (DEV)
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

        self.args = parser.parse_args()

    def gen_bq_coors(self):
        # try:
        start_pos = input('\nEnter coordinates (x, y, z) for first ghost atom separated by spaces: ')
        vec_space = input('Specify vector spacings (x, y, z) separated by spaces: ')
        bq_no = int(input('Specify the number of ghost atoms (in 1 dimension): '))

        origin = numpy.array(start_pos.split(), float)
        vs_split = numpy.array(vec_space.split(), float)

        x_vec = numpy.array([vs_split[0], 0, 0])
        y_vec = numpy.array([0, vs_split[1], 0])
        z_vec = numpy.array([0, 0, vs_split[2]])

        print(x_vec)
        print(y_vec)
        print(z_vec)

        if x_vec == numpy.any([0, 0, 0]):
            array_1 = y_vec
            array_2 = z_vec
        elif y_vec == numpy.any([0, 0, 0]):
            array_1 = x_vec
            array_2 = z_vec
        elif z_vec == numpy.any([0, 0, 0]):
            array_1 = x_vec
            array_2 = y_vec

        print(array_1)
        print(array_2)

        for n1 in range(numpy.nonzero(array_1), bq_no):
            for n2 in range(numpy.nonzero(array_2), bq_no):
                self.bq_coors += [origin + n1 * array_1 + n2 * array_2]

        if self.args.verbose is True:
            print('\nOutput:\n')  # Shows usr list of coors generated
            print(*self.bq_coors, sep='\n')  # Is there a way to pipe this to less instead? eg. print... | less
        '''
        except (IndexError, ValueError) as error:
            print('\nThere was an error in interpreting your input:')
            print(error)
            print('\nPlease try again:')
            self.bq_coors.clear()
            self.gen_bq_coors()
            '''

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
