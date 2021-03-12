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
            # Will only work if 3rd direction == 0

            start = numpy.array(start_pos.split(), float)
            end = numpy.array(end_pos.split(), float)
            vs = numpy.array(vec_space.split(), float)

            if self.args.xy_plane is True:
                vec1 = numpy.array([vs[0], 0, 0])
                vec2 = numpy.array([0, vs[1], 0])
                const = numpy.array([0, 0, vs[2]])
            elif self.args.xz_plane is True:
                vec1 = numpy.array([vs[0], 0, 0])
                vec2 = numpy.array([0, 0, vs[2]])
                const = numpy.array([0, vs[1], 0])
            elif self.args.yz_plane is True:
                vec1 = numpy.array([0, vs[1], 0])
                vec2 = numpy.array([0, 0, vs[2]])
                const = numpy.array([vs[0], 0, 0])
            # vec spaces specified in different locations in variables depending on which plane arg is selected by usr

            coors = []
            origin = numpy.array([0, 0, 0])

            for n1 in range(int(start[0]), int(end[0])):
                for n2 in range(int(start[1]), int(end[1])):  # Fix problem with not working for planes other than xy
                    coors += [origin + n1*vec1 + n2*vec2 + const]

            print(coors)

            for coor in coors:
                self.bq_coors.append(f'Bq {coor[0]} {coor[1]} {coor[2]}')

            if self.args.verbose is True:
                print('\nOutput:\n')
                print(*self.bq_coors, sep='\n')  # Is there a way to pipe this to less instead? eg. print... | less
                # Shows usr list of coors generated

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
