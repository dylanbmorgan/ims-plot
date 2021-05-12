#!/usr/bin/env python3
# 1d_graph_plotter.py
# Plots graph of isotropic NICS values from parsed data file
# Author: Dylan Morgan

import matplotlib.pyplot as plt
import argparse
import glob
import sys


class Plotter:

    def __init__(self):
        self.x_values = []
        self.y_values = []
        self.y_axis_label = '\u03B4 / ppm'

    def cli_cmds(self):
        def formatter(prog):
            return argparse.HelpFormatter(prog, max_help_position=80)

        parser = argparse.ArgumentParser(formatter_class=formatter,
                                         description='Plots a graph to show isotropic NICS values from parsed '
                                         'Gaussian log file data')
        parser.add_argument('-f', '--filename',
                            nargs='?',
                            default=glob.glob('.parsed_data*.txt'),
                            # ^^ Might not work if a different file is specified other than default
                            help='if a custom file name was given for the parsed log data, use this flag to '
                            'specify the name of that file')
        parser.add_argument('-s', '--shielding',
                            action='store_true',
                            help='plot graph as a function of isotropic magnetic shielding instead of chemical shift')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='print the values of the x and y axes of the plot')

        axis_group = parser.add_mutually_exclusive_group(required=True)

        axis_group.add_argument('-x', '--xaxis',
                                action='store_true',
                                help='specify the direction the ghost atoms are plotted in as the x-axis')
        axis_group.add_argument('-y', '--yaxis',
                                action='store_true',
                                help='specify the direction the ghost atoms are plotted in as the y-axis')
        axis_group.add_argument('-z', '--zaxis',
                                action='store_true',
                                help='specify the direction the ghost atoms are plotted in as the z-axis')

        self.args = parser.parse_args()

    def append_coors(self):
        if self.args.xaxis is True:
            value = 3
        elif self.args.yaxis is True:
            value = 4
        elif self.args.zaxis is True:
            value = 5

        try:
            for file in self.args.filename:
                with open(file) as data:
                    for line in data:
                        words = line.split()
                        if 'cBq:' in line:
                            self.x_values.append(float(words[value]))  # Bq coors
                        elif 'iBq:' in line:
                            self.y_values.append(float(words[2]))  # isotropic values

        except (FileNotFoundError, ValueError, IndexError) as error:
            print('\nThere was an issue with reading the parsed data:')
            print(error)
            sys.exit()

    def check_arrays(self):
        if self.x_values == [] and self.y_values == []:  # error catching
            print(f'\nError: {self.args.file} is missing the lines containing cBq and iBq (ghost atom coordinates and '
                  'isotropic NICS values')
            sys.exit()
        elif self.x_values == []:
            print(f'\nError: {self.args.file} is missing the lines containing cBq (ghost atom coordinates)')
            sys.exit()
        elif self.y_values == []:
            print(f'\nError: {self.args.file} is missing the lines containing iBq (isotropic NICS values)')
            sys.exit()

        if self.args.shielding is True:
            self.y_axis_label = 'Isotropic Magnetic Shielding Tensor / ppm'
            pass
        else:
            for chg_sign, num in enumerate(self.y_values):
                self.y_values[chg_sign] = num * -1

    def draw_plot(self):
        if self.args.verbose is True:
            print('x-axis:', *self.x_values, sep=' ')
            print('y-axis:', *self.y_values, sep=' ')

        try:
            x = self.x_values  # x-values; where the atoms are
            y = self.y_values  # The isotropic NICS values
            plt.plot(x, y)  # Plotting the points
            plt.xlabel('Distance / \u212B', fontsize=16)
            plt.ylabel(self.y_axis_label, fontsize=16)
            plt.tick_params(axis='both', which='both', labelsize=12)
            plt.show()
            # TODO: incorporate a feature to present multiple 1D arrays on a single graph

        except (ValueError, IndexError) as error:
            print('\nThere was an error with plotting the graph:')
            print(error)


if __name__ == '__main__':
    p = Plotter()
    p.cli_cmds()
    p.append_coors()
    p.check_arrays()
    p.create_plot()
