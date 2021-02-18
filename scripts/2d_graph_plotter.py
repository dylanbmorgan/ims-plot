#!/usr/bin/env python3
# 2d_graph_plotter.py
# Plots contour plot of isotropic NICS values from parsed file data
# Author: Dylan Morgan

import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys


class plotter:

    def __init__(self):
        self.x_values = []
        self.y_values = []
        self.z_values = []

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

        parser.add_argument('-f', '--file',
                            action='store_true',
                            default='.parsed_log_data.txt',
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
            with open(self.args.file) as data:
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

        if self.x_values == [] and self.z_values == []:
            print(f'\nError: {self.args.file} is missing the lines containing cBq and iBq (ghost atom coordinates and '
                  'isotropic NICS values')
            sys.exit()
        elif self.x_values == [] or self.y_values == []:
            print(f'\nError: {self.args.file} is missing the lines containing cBq (ghost atom coordinates)')
            sys.exit()
        elif self.z_values == []:
            print(f'\nError: {self.args.file} is missing the lines containing iBq (isotropic NICS values)')
            sys.exit()

        if self.args.verbose is True:
            print('x-axis:', *self.x_values, sep=' ')
            print('y-axis:', *self.y_values, sep=' ')
            print('z-axis:', *self.z_values, sep=' ')

    def create_plot(self):
        try:
            # for num in self.x_values:
            #    x_list = np.linspace(num)

            # for num in self.y_values:
            #    y_list = np.linspace(num)

            X, Y, Z = np.meshgrid(self.x_values, self.y_values, self.z_values)
            fig, ax = plt.subplots()
            CP = ax.contour(X, Y, Z)  # see: https://stackoverflow.com/questions/34113083/numpy-contour-typeerror-input-z-must-be-a-2d-array
            ax.clabel(CP, inline=1, fontsize=10)
            ax.set_title('Simplest default with labels')

        except (ValueError, IndexError) as error:
            print('\nThere was an error with plotting then graph:')
            print(error)


if __name__ == '__main__':
    p = plotter()
    p.cli_cmds()
    p.append_coors()
    p.create_plot()
