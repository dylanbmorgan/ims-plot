#!/usr/bin/env python3
# 2D Ghost Atom Generator
# 2d_ga_gen.py
# Generates 2D array of Bq atoms for Gaussian input files
# Authors: Dylan Morgan & Dr Felix Plasser

import numpy
import argparse
import glob


class InputGenerator:

    def __init__(self):
        self.bq_coors = []
        # self.all_bqs = []

    def cli_cmds(self):
        parser = argparse.ArgumentParser(description='Generates Bq atoms for Gaussian input files in 2D')
        parser.add_argument('originalfile', help='original file to copy')
        parser.add_argument('newfile', help='new file to write to (do not include the file extension)')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='print output of Bq coordinates to append to file')

        '''
        TODO: Integrate the following:
        parser.add_argument('-c', '--connectivity',
                            action='store_true',
                            help='Include information for ghost atoms as part of geom=connectivity if this is to be'
                            'used') '''

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
            vec_space = input('Specify the 2 vector spacings separated by spaces: ')

            start = numpy.array(start_pos.split(), float)
            end = numpy.array(end_pos.split(), float)
            vs = numpy.array(vec_space.split(), float)

            if self.args.xy_plane is True:
                s_coor_1 = start[0]
                s_coor_2 = start[1]
                e_coor_1 = end[0]
                e_coor_2 = end[1]
                vec1 = numpy.array([1., 0., 0.])  # Always has to be 1
                vec2 = numpy.array([0., 1., 0.])

            elif self.args.xz_plane is True:
                s_coor_1 = start[0]
                s_coor_2 = start[2]
                e_coor_1 = end[0]
                e_coor_2 = end[2]
                vec1 = numpy.array([1, 0., 0.])
                vec2 = numpy.array([0., 0., 1])

            elif self.args.yz_plane is True:
                s_coor_1 = start[1]
                s_coor_2 = start[2]
                e_coor_1 = end[1]
                e_coor_2 = end[2]
                vec1 = numpy.array([0., 1, 0.])
                vec2 = numpy.array([0., 0., 1])
            # vec spaces specified in different locations in variables depending on which plane arg is selected by usr

            coors = []

            for i in numpy.arange(s_coor_1, e_coor_1 + vs[0], vs[0]):
                for j in numpy.arange(s_coor_2, e_coor_2 + vs[1], vs[1]):
                    coors += [i*vec1 + j*vec2]
                    # Auto generates all Bq coors based off usr start and end coors
                    # Auto defines no of Bqs based off usr vec spacings

            for num in coors:
                self.bq_coors.append(f'Bq {num[0]} {num[1]} {num[2]}')

            if self.args.verbose is True:
                print('\nOutput:\n')
                print(*self.bq_coors, sep='\n')
                print(f'\nTotal number of ghost atoms: {len(self.bq_coors)}')  # Print coors in column format

        except (IndexError, ValueError, TypeError) as error:
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
            self.all_bqs.clear()
            self.gen_bq_coors()
            ig.check_1()
        else:
            print('Not a valid answer')
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

    def copy_inp(self):
        with open(self.args.originalfile) as originalfile:

            def split_lines_gen(lines):
                for coors in range(0, len(lines), 100):
                    yield lines[coors: coors + 100]

            for index, lines in enumerate(split_lines_gen(self.bq_coors)):
                with open(f'./{str(self.args.newfile)}_{str(index + 1)}.com', 'w') as nextfile:
                    nextfile.write('\n'.join(lines))
                    nextfile.write('\n ')

            with open(glob.glob(f'./{self.args.newfile}_[1-9].com'), 'w+') as file:
                file.seek(0, 0)
                for line in originalfile:
                    file.write(line)

        if self.args.verbose is True:
            with open(f'*{self.args.newfile}*', 'r') as copy:  # fix this bit
                # if copy.mode == 'r':
                contents = copy.read()
                print(f'\nContents of file(s):\n\n{contents}')

        print('Task completed successfully!')
        print('Remember to fill in the geom=connectivity information in the generated file')


if __name__ == '__main__':
    ig = InputGenerator()
    ig.cli_cmds()
    ig.gen_bq_coors()
    ig.check_1()
    # ig.enumerate_geom()
    # ig.check_2()
    ig.copy_inp()
