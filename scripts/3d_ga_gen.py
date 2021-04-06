#!/usr/bin/env python3
# 3D Ghost Atom Generator
# 3d_ga_gen.py
# Generates 3D array of Bq atoms for Gaussian input files
# Authors: Dylan Morgan & Dr Felix Plasser

import numpy
import argparse


class InputGenerator:

    def __init__(self):
        self.bq_coors = []
        # self.all_bqs = []

    def cli_cmds(self):
        parser = argparse.ArgumentParser(description='Generates Bq atoms for Gaussian input files in 3D')
        parser.add_argument('startfile', help='original file to copy')
        parser.add_argument('newfiles', help='new file to write to')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='print output of Bq coordinates to append to file')

        '''
        TODO: Integrate the following:
        parser.add_argument('-c', '--connectivity',
                            action='store_true',
                            help='Include information for ghost atoms as part of geom=connectivity if this is to be'
                            'used') '''

        self.args = parser.parse_args()

    # TODO: Add argparse to generate ghost atoms in the same way as the 2d script

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
                        self.bq_coors.append(f'Bq {nx[0]} {ny[1]} {nz[2]}')
                        # Adds each coor as new line in new file

            if self.args.verbose is True:
                print('\nOutput:\n')  # Shows usr list of coors generated
                print(*self.bq_coors, sep='\n')
                print(f'\nTotal number of ghost atoms: {len(self.bq_coors)}')  # Print coors in column format

        except (IndexError, ValueError) as error:
            print('\nThere was an error in interpreting your input:')
            print(error)
            print('\nPlease try again (or press ctrl+c to exit):')
            self.bq_coors.clear()
            self.gen_bq_coors()

    def check_1(self):
        cont = input('\nProceed? (y/n) ')

        if cont.lower() == 'y' or cont.lower() == 'yes':
            pass
        elif cont.lower() == 'n' or cont.lower() == 'no':
            self.bq_coors.clear()
            # self.all_bqs
            self.gen_bq_coors()
            ig.check_1()
        else:
            print('\nNot a valid answer')
            ig.check_1()

    def enumerate_geom(self):
        try:
            index = 0
            index = int(input('\nSpecify the number of non-Bq atoms to be defined in geom=connectivity: '))

        except (IndexError, ValueError) as error:
            print('\nThere was an error in interpreting your input:')
            print(error)
            print('\nPlease try again (or press ctrl+c to exit):')
            self.enumerate_geom()

        for line in self.bq_coors:
            index += 1
            self.all_bqs.append(index)
            # Auto generates atoms for geom=connectivity
            # Tells Gaussian not to form bonds between Bqs

        # TODO: Remove the last nums from the list specified by the usr

        if self.args.verbose is True:
            print()
            print(*self.all_bqs, sep='\n')  # Print

    def check_2(self):
        cont = input('\nProceed? (y/n) ')

        if cont.lower() == 'y' or cont.lower() == 'yes':
            pass
        elif cont.lower() == 'n' or cont.lower() == 'no':
            self.enumerate_geom()
            ig.check_2()
        else:
            print('Not a valid answer')
            ig.check_2()

    def write_files(self):
        def split_lines_gen(lines):
            for coors in range(0, len(lines), 99):
                yield lines[coors: coors + 99]

        for index, lines in enumerate(split_lines_gen(self.bq_coors)):
            with open(f'./{str(self.args.newfiles)}_{str(index + 1)}.com', 'w+') as newfiles:
                with open(self.args.startfile) as start:
                    for info in start:
                        newfiles.write(info)

                newfiles.write('\n'.join(lines))
                newfiles.write('\n ')

        print('\nTask completed successfully!')
        # print('Remember to fill in the geom=connectivity information in the generated file')


if __name__ == '__main__':
    ig = InputGenerator()
    ig.cli_cmds()
    ig.gen_bq_coors()
    ig.check_1()
    # ig.enumerate_geom()
    # ig.check_2()
    ig.write_files()
