#!/usr/bin/env python3
# 2D Ghost Atom Generator
# 2d_ga_gen.py
# Generates 2D array of Bq atoms for Gaussian input files
# Authors: Dylan Morgan & Dr Felix Plasser

import argparse
import numpy as np


class InputGenerator:

    def __init__(self):
        self.bq_coors = []

    def cli_cmds(self):
        def formatter(prog):
            return argparse.HelpFormatter(prog, max_help_position=80)

        parser = argparse.ArgumentParser(formatter_class=formatter,
                                         description='Generates Bq atoms for Gaussian input files in 2D')
        parser.add_argument('startfile', help='original file to copy')
        parser.add_argument('newfiles', help='new file(s) to write to (do not include the file extension)')
        parser.add_argument('-c', '--chkfile',
                            action='store_true',
                            help='include a line in the input file(s) which will generate a Gassian .chk file in '
                            'addition to a .log file (MUST ALREADY have a line specifying nprocs as per the Guassian '
                            'manual)')
        parser.add_argument('-n', '--number',
                            type=int,
                            nargs='?',
                            default=25,
                            help='specify the number of ghost atoms to write per file (default = 25). It might be '
                            'useful to reduce this value if any of jobs fail when running on Gaussian')
        parser.add_argument('-v', '--verbose',
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
            start_pos = input('\nEnter start coordinates (x, y, z) for the first ghost atom separated by spaces: ')
            end_pos = input('Enter end coordinates (x, y, z) for the last ghost atom separated by spaces: ')
            vec_space = input('Specify the 2 vector spacings separated by spaces: ')

            start = np.array(start_pos.split(), float)
            end = np.array(end_pos.split(), float)
            vs = np.array(vec_space.split(), float)

            if self.args.xy_plane is True:
                s_coor_1 = start[0]
                s_coor_2 = start[1]
                e_coor_1 = end[0]
                e_coor_2 = end[1]
                vec1 = np.array([1., 0., 0.])  # Always have to be 1
                vec2 = np.array([0., 1., 0.])
                const = np.array([0., 0., start[2]])

            elif self.args.xz_plane is True:
                s_coor_1 = start[0]
                s_coor_2 = start[2]
                e_coor_1 = end[0]
                e_coor_2 = end[2]
                vec1 = np.array([1, 0., 0.])
                vec2 = np.array([0., 0., 1])
                const = np.array([0., start[1], 0.])

            elif self.args.yz_plane is True:
                s_coor_1 = start[1]
                s_coor_2 = start[2]
                e_coor_1 = end[1]
                e_coor_2 = end[2]
                vec1 = np.array([0., 1, 0.])
                vec2 = np.array([0., 0., 1])
                const = np.array([start[0], 0., 0.])
            # vec spaces specified in different locations in variables depending on which plane arg is selected by usr

            coors = []
            arr_x = np.arange(s_coor_1, e_coor_1 + vs[0], vs[0])
            arr_y = np.arange(s_coor_2, e_coor_2 + vs[1], vs[1])

            for i in arr_x:
                for j in arr_y:
                    coors += [i * vec1 + j * vec2 + const]
                    # Auto generates all Bq coors based off usr start and end coors
                    # Auto defines no of Bqs based off usr vec spacings

            for num in coors:
                self.bq_coors.append(f'Bq {num[0]} {num[1]} {num[2]}')

            if self.args.verbose is True:
                print('\nOutput:\n')
                print(*self.bq_coors, sep='\n')
                print(f'\nTotal number of ghost atoms: {len(self.bq_coors)}')
                # Print coors in column format

            x_len = len(arr_x)
            y_len = len(arr_y)

            with open('input_data.txt', 'w') as gen_data:
                gen_data.write(f'dim_x = {x_len}\ndim_y = {y_len}\n'
                               f'min_x = {s_coor_1}\nmin_y = {s_coor_2}\n'
                               f'step_x = {vs[0]}\nstep_y = {vs[1]}')

        except (IndexError, ValueError, TypeError) as error:
            print('\nThere was an error in interpreting your input:')
            print(error)
            print('\nPlease try again (or press ctrl+c to exit):')
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
            print('\nNot a valid answer')
            ig.check()

    def write_files(self):
        def split_lines_gen(lines):
            for coors in range(0, len(lines), self.args.number):
                yield lines[coors:coors + self.args.number]

        total_files = []

        for index, lines in enumerate(split_lines_gen(self.bq_coors)):
            if index == 0:
                file_location = f'./{str(self.args.newfiles)}.com'
                # TODO: Prevent 1st file from being unnumbered if > 1 is created

            else:
                file_location = f'./{str(self.args.newfiles)}_{str(index + 1)}.com'

            with open(file_location, 'w+') as newfile:
                total_files.append(newfile)
                # TODO: add lines to remove last line of file if empty

                with open(self.args.startfile) as start:
                    for info in start:
                        newfile.write(info)

                        if self.args.chkfile is True and 'nproc' in info:
                            newfile.write(f'%chk=./{str(self.args.newfiles)}_{str(index + 1)}.chk\n')

                newfile.write('\n'.join(lines))
                newfile.write('\n ')

        print(f'\nTask completed successfully!\n{len(total_files)} new file(s) were created.')


if __name__ == '__main__':
    ig = InputGenerator()
    ig.cli_cmds()
    ig.gen_bq_coors()
    ig.check()
    ig.write_files()
