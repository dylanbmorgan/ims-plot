#!/usr/bin/env python3
# 2D Ghost Atom Generator
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
            start_pos = input('\nEnter start coordinates (x, y, z) for first ghost atom separated by spaces: ')
            end_pos = input('Enter end coordinates (x, y, z) for the last ghost atom separated by spaces: ')
            vec_space = input('Specify vector spacings (x, y, z) separated by spaces: ')

            start = numpy.array(start_pos.split(), int)
            end = numpy.array(end_pos.split(), int)
            vs = numpy.array(vec_space.split(), float)

            if self.args.xy_plane is True:
                s_coor_1 = start[0]
                s_coor_2 = start[1]
                e_coor_1 = end[0]
                e_coor_2 = end[1]
                vec1 = numpy.array([vs[0], 0., 0.])
                vec2 = numpy.array([0., vs[1], 0.])
                const = numpy.array([0., 0., start[2]])  # for plane not used for usr to specify dist from origin plane
                range_add_1 = vs[0]
                range_add_2 = vs[1]

            elif self.args.xz_plane is True:
                s_coor_1 = start[0]
                s_coor_2 = start[2]
                e_coor_1 = end[0]
                e_coor_2 = end[2]
                vec1 = numpy.array([vs[0], 0., 0.])
                vec2 = numpy.array([0., 0., vs[2]])
                const = numpy.array([0., start[1], 0.])
                range_add_1 = vs[0]
                range_add_2 = vs[2]

            elif self.args.yz_plane is True:
                s_coor_1 = start[1]
                s_coor_2 = start[2]
                e_coor_1 = end[1]
                e_coor_2 = end[2]
                vec1 = numpy.array([0., vs[1], 0.])
                vec2 = numpy.array([0., 0., vs[2]])
                const = numpy.array([start[0], 0., 0.])
                range_add_1 = vs[1]
                range_add_2 = vs[2]
            # vec spaces specified in different locations in variables depending on which plane arg is selected by usr

            coors = []

            for i in range(s_coor_1, e_coor_1 + int(range_add_1)):
                for j in range(s_coor_2, e_coor_2 + int(range_add_2)):
                    coors += [i*vec1 + j*vec2 + const]

            for num in coors:
                self.bq_coors.append(f'Bq {num[0]} {num[1]} {num[2]}')

            if self.args.verbose is True:
                print('\nOutput:\n')
                print(*self.bq_coors, sep='\n')
                # Shows usr list of coors generated in column

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
