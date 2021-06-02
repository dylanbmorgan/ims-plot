#!/usr/bin/env python3
# 1D Ghost Atom Generator
# 1d_ga_gen.py
# Generates 1D array of Bq atoms for Gaussian input files
# Authors: Dylan Morgan & Dr Felix Plasser

import numpy
import argparse


class InputGenerator:

    def __init__(self):
        self.bq_coors = []

    def cli_cmds(self):
        def formatter(prog):
            return argparse.HelpFormatter(prog, max_help_position=80)

        parser = argparse.ArgumentParser(formatter_class=formatter,
                                         description='Generates array of Bq atoms for Gaussian input files in 1D')
        parser.add_argument('startfile', help='original file to copy')
        parser.add_argument('newfiles', help='new file(s) to write to (do not include the file extension)')
        parser.add_argument('-c', '--chkfile',
                            action='store_true',
                            help='include a line in the input file(s) which will generate a Gassian .chk file in '
                            'addition to a .log file (MUST ALREADY have a line specifying nprocs as per the Guassian '
                            'manual)')
        parser.add_argument('-d', '--define_spacings',
                            action='store_true',
                            help='generate ghost atoms by defining vector spacings rather than start and end '
                            'coordinates')
        parser.add_argument('-n', '--number',
                            type=int,
                            nargs='?',
                            default=100,
                            help='specify the number of ghost atoms to write per file (default = 100). It might be '
                            'useful to reduce this value if any of jobs fail when running on Gaussian')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='print output of Bq coordinates to append to file')

        plane = parser.add_mutually_exclusive_group(required=True)

        plane.add_argument('-x', '--x_direction',
                           action='store_true',
                           help='specify the direction of the array in the x-direction')
        plane.add_argument('-y', '--y_direction',
                           action='store_true',
                           help='specify the direction of the array in the y-direction ')
        plane.add_argument('-z', '--z_direction',
                           action='store_true',
                           help='specify the direction of the array in the z-direction')

        self.args = parser.parse_args()

    def gen_bq_coors(self):
        try:
            if self.args.define_spacings is True:
                coor = input('\nEnter coordinates (x, y, z) for the first ghost atom separated by spaces: ')
                vs = input('Specify vector spacings (x, y, z) separated by spaces: ')
                bq_no = int(input('Specify number of ghost atoms: '))

                x0 = numpy.array(coor.split(), float)
                deltaxyz = numpy.array(vs.split(), float)

                for n in range(bq_no):
                    xn = x0 + n * deltaxyz
                    self.bq_coors.append(f'Bq {xn[0]} {xn[1]} {xn[2]}')

            else:
                start_pos = input('\nEnter start coordinates (x, y, z) for the first ghost atom separated by spaces: ')
                end_pos = input('Enter end coordinates (x, y, z) for the last ghost atom separated by spaces: ')
                vs = float(input('Specify the 1D vector spacings: '))

                start = numpy.array(start_pos.split(), float)
                end = numpy.array(end_pos.split(), float)

                if self.args.x_direction is True:
                    s_coor = start[0]
                    e_coor = end[0]
                    vec = numpy.array([1., 0., 0.])  # Always have to be 1
                    const = numpy.array([0., start[1], start[2]])

                if self.args.y_direction is True:
                    s_coor = start[1]
                    e_coor = end[1]
                    vec = numpy.array([0., 1., 0.])
                    const = numpy.array([start[0], 0., start[2]])

                if self.args.z_direction is True:
                    s_coor = start[2]
                    e_coor = end[2]
                    vec = numpy.array([0., 0., 1.])
                    const = numpy.array([start[0], start[1], 0.])

                coors = []

                for i in numpy.arange(s_coor, e_coor + vs, vs):
                    coors += [i * vec + const]
                    # Auto generates all Bq coors based off usr start and end coors
                    # Auto defines no of Bqs based off usr vec spacings

                for num in coors:
                    self.bq_coors.append(f'Bq {num[0]} {num[1]} {num[2]}')

                if self.args.verbose is True:
                    print('\nOutput:\n')
                    print(*self.bq_coors, sep='\n')  # Print coors in column format
                    print(f'\nTotal number of ghost atoms: {len(self.bq_coors)}')

        except (IndexError, ValueError) as error:  # Should catch all errors that arise
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
                # TODO: add code to remove last line of file if empty

                with open(self.args.startfile) as start:
                    for info in start:
                        newfile.write(info)

                        if self.args.chkfile is True and 'nproc' in info:
                            newfile.write(f'%chk=./{str(self.args.newfiles)}_{str(index + 1)}.chk\n')
                            # Adds line to generate chk file if specified in cli arg

                newfile.write('\n'.join(lines))
                newfile.write('\n ')

        print(f'\nTask completed successfully!\n{len(total_files)} new file(s) were created.')


if __name__ == '__main__':
    ig = InputGenerator()
    ig.cli_cmds()
    ig.gen_bq_coors()
    ig.check()
    ig.write_files()
