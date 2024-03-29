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

    def cli_cmds(self):
        def formatter(prog):
            return argparse.HelpFormatter(prog, max_help_position=80)

        parser = argparse.ArgumentParser(formatter_class=formatter,
                                         description='Generates Bq atoms for Gaussian input files in 3D')
        parser.add_argument('startfile', help='original file to copy')
        parser.add_argument('newfiles', help='new file(s) to write to (do not include the file extension)')
        parser.add_argument('-c', '--nochk',
                            action='store_false',
                            help='prevent lines being added to the input file(s) which would generate a Gaussian .chk '
                            'file in addition to a .log file.')
        parser.add_argument('-d', '--define_spacings',
                            action='store_true',
                            help='generate ghost atoms by defining vector spacings rather than start and end '
                            'coordinates')
        parser.add_argument('-n', '--number',
                            type=int,
                            nargs='?',
                            default=25,
                            help='specify the number of ghost atoms to write per file (default = 25). It might be '
                            'useful to reduce this value if any of jobs fail when running on Gaussian')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='print output of Bq coordinates to append to file')

        self.args = parser.parse_args()

    def gen_bq_coors(self):
        try:
            if self.args.define_spacings is True:
                coor = input('\nEnter coordinates (x, y, z) for the first ghost atom separated by spaces: ')
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

            else:
                start_pos = input('\nEnter start coordinates (x, y, z) for the first ghost atom separated by spaces: ')
                end_pos = input('Enter end coordinates (x, y, z) for the last ghost atom separated by spaces: ')
                vec_space = input('Specify the 3 vector spacings separated by spaces: ')

                start = numpy.array(start_pos.split(), float)
                end = numpy.array(end_pos.split(), float)
                vs = numpy.array(vec_space.split(), float)

                vec1 = numpy.array([1., 0., 0.])  # Always have to be 1
                vec2 = numpy.array([0., 1., 0.])
                vec3 = numpy.array([0., 0., 1.])
                const = numpy.array([0., 0., 0.])

                coors = []

                for i in numpy.arange(start[0], end[0] + vs[0], vs[0]):
                    for j in numpy.arange(start[1], end[1] + vs[1], vs[1]):
                        for k in numpy.arange(start[2], end[2] + vs[2], vs[2]):
                            coors += [i * vec1 + j * vec2 + k * vec3 + const]
                            # Auto generates all Bq coors based off usr start and end coors
                            # Auto defines no of Bqs based off usr vec spacings

                for num in coors:
                    self.bq_coors.append(f'Bq {num[0]} {num[1]} {num[2]}')

            if self.args.verbose is True:
                print('\nOutput:\n')
                print(*self.bq_coors, sep='\n')  # Print coors in column format
                print(f'\nTotal number of ghost atoms: {len(self.bq_coors)}')

        except (IndexError, ValueError) as error:
            print('\nThere was an error in interpreting your input:')
            print(error)
            print('\nPlease try again (or press ctrl+c to exit):')
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

                        if self.args.nochk is not True:
                            if 'nproc' in info:
                                newfile.write(f'%chk=./{str(self.args.newfiles)}_{str(index + 1)}.chk\n')

                newfile.write('\n'.join(lines))
                newfile.write('\n ')

        print(f'\nTask completed successfully!\n{len(total_files)} new files were created.')


if __name__ == '__main__':
    ig = InputGenerator()
    ig.cli_cmds()
    ig.gen_bq_coors()
    ig.check()
    ig.write_files()
