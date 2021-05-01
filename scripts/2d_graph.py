#!/usr/bin/env python3
# 2d_graph_plotter.py
# Plots contour plot of isotropic NICS values from parsed file data
# Author: Dylan Morgan

import matplotlib.pyplot as plt
import argparse
import glob
import sys


class Plotter:

    def __init__(self):
        self.x_values = []
        self.y_values = []
        self.z_values = []
        self.z_axis_label = '\u03B4 / ppm'

    def cli_cmds(self):
        parser = argparse.ArgumentParser(description='Plots a contour plot to show isotropic NICS values from '
                                         'parsed Gaussian log file data')
        axis_group = parser.add_mutually_exclusive_group(required=True)

        axis_group.add_argument('-xy', '--xyplane',
                                action='store_true',
                                help='specify the plane the ghost atoms are plotted in as the xy-plane')
        axis_group.add_argument('-yz', '--yzplane',
                                action='store_true',
                                help='specify the plane the ghost atoms are plotted in as the yz-plane')
        axis_group.add_argument('-xz', '--xzplane',
                                action='store_true',
                                help='specify the plane the ghost atoms are plotted in as the xz-plane')

        parser.add_argument('-sh', '--shielding',
                            action='store_true',
                            help='plot graph as a function of isotropic magnetic shielding instead of chemical shift')
        parser.add_argument('-f', '--filename',
                            nargs='?',
                            default=glob.glob('.parsed_data*.txt'),
                            # ^^ Might not work if a different file is specified other than default
                            help='if a custom file name was given for the parsed log data, use this flag to '
                            'specify the name of that file')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='print the values of the x and y axes of the plot')
        self.args = parser.parse_args()

    def append_coors(self):
        if self.args.xyplane is True:
            axis_x = 3
            axis_y = 4
        elif self.args.yzplane is True:
            axis_x = 4
            axis_y = 5
        elif self.args.xzplane is True:
            axis_x = 3
            axis_y = 5

        try:
            for file in self.args.filename:
                with open(file) as data:  # Might not work yet if only 1 file is specified
                    for line in data:
                        words = line.split()
                        if 'cBq' in line:
                            self.x_values.append(float(words[axis_x]))
                            self.y_values.append(float(words[axis_y]))
                        elif 'iBq' in line:
                            self.z_values.append(float(words[2]))

        except (FileNotFoundError, ValueError, IndexError) as error:
            print('\nThere was an issue with reading the parsed data:')
            print(error)
            sys.exit()

    def check_arrays(self):
        if self.x_values == [] and self.z_values == []:
            print(f'\nError: {self.args.filename} is/are missing the lines containing cBq and iBq (ghost atom '
                  'coordinates and isotropic NICS values)')
            sys.exit()
        elif self.x_values == [] or self.y_values == []:
            print(f'\nError: {self.args.filename} is/are missing the lines containing cBq (ghost atom coordinates)')
            sys.exit()
        elif self.z_values == []:
            print(f'\nError: {self.args.filename} is/are missing the lines containing iBq (isotropic NICS values)')
            sys.exit()

        if self.args.shielding is True:
            self.z_axis_label = 'Isotropic Magnetic Shielding Tensor / ppm'
        else:
            for chg_sign, num in enumerate(self.z_values):
                self.z_values[chg_sign] = num * -1

    def draw_plot(self):
        if self.args.verbose is True:
            self.x_values.insert(0, 'x-values')
            self.y_values.insert(0, 'y-values')
            self.z_values.insert(0, 'z-values')

            for x, y, z in zip(self.x_values, self.y_values, self.z_values):
                print(x, y, z)  # Prints arrays as columns

            del self.x_values[0]
            del self.y_values[0]
            del self.z_values[0]

        x = self.x_values
        y = self.y_values
        z = self.z_values

        try:
            plt.tricontourf(x, y, z)
            # plt.clabel(cp)
            plt.show()

        except (ValueError, IndexError) as error:
            print('\nThere was an error with plotting the graph:')
            print(error)


if __name__ == '__main__':
    p = Plotter()
    p.cli_cmds()
    p.append_coors()
    p.check_arrays()
    p.draw_plot()
