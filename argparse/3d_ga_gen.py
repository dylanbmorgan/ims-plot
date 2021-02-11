#!/usr/bin/python

import numpy


class input_generator:

    def __init__(self):
        self.bq_coors = []

    def gen_bq_coors(self):
        coor = input('\nEnter coordinates (x, y, z) for first ghost atom separated by spaces: ')
        vs = input('Specify vector spacings (x, y, z) separated by spaces: ')
        bq_no = int(input('Specify number of ghost atoms (in 1 dimension): '))

        n0 = numpy.array(coor.split(), float)
        deltaxyz = numpy.array(vs.split(), float)
        deltax = numpy.array([deltaxyz[0], 0, 0])
        deltay = numpy.array([0, deltaxyz[1], 0])
        deltaz = numpy.array([0, 0, deltaxyz[2]])

        for xn in range(bq_no):
            nx = n0 + xn * deltax

            for yn in range(bq_no):
                ny = n0 + yn * deltay

                for zn in range(bq_no):
                    nz = n0 + zn * deltaz
                    self.bq_coors.append(f'Bq {nx[0]} {ny[1]} {nz[2]}')

        print('\n')
        print('Output:\n')
        print(*self.bq_coors, sep='\n')

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
        original_filename = input("\nFile to copy (must be full path):\n")
        copy_filename = input("\nName to save copy as (must be full path):\n")

        with open(original_filename) as original:
            with open(copy_filename, "w+") as copy:

                for line in original:
                    copy.write(line)

                for coor in self.bq_coors:
                    copy.write(f'{coor}\n')
                    copy.write('')

        with open(copy_filename, "r") as copy:

            if copy.mode == "r":
                contents = copy.read()
                print(contents)


if __name__ == '__main__':
    ig = input_generator()
    ig.gen_bq_coors()
    ig.check()
    ig.copy_inp()
