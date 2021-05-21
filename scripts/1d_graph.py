#!/usr/bin/env python3
# 1d_graph_plotter.py
# Plots graph of isotropic NICS values from parsed data file
# Author: Dylan Morgan

import argparse
# import glob
import matplotlib.pyplot as plt
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
                            # default=glob.glob('parsed_data*.txt'),
                            # TODO: give default args for -f and -m
                            nargs='+',
                            type=argparse.FileType('r'),
                            help='if a custom file name was given for the parsed log data, use this flag to '
                            'specify the name of that file')
        parser.add_argument('-m', '--multi_plot',
                            # default=glob.glob('parsed_data*.txt'),
                            nargs='+',
                            type=argparse.FileType('r'),
                            help='use this option with multiple parsed data files to plot multiple jobs on the '
                            'same graph (this currently does not work with jobs that have been split into multiple '
                            'files and custom filenames will have to be used for parsed log data)')
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
            if not self.args.multi_plot:  # Check if list is empty
                nonrounded_x = []

                for file in self.args.filename:
                    for line in file:
                        words = line.split()
                        if 'cBq:' in line:
                            nonrounded_x.append(float(words[value]))  # Bq coors

                        elif 'iBq:' in line:
                            self.y_values.append(float(words[2]))  # Isotropic values

                self.x_values = [round(num, 3) for num in nonrounded_x]

            else:
                bq_coor_dict = {}
                multi_plot_index = {}
                iso_dict = {}
                # Use dictionaries to create x number of lists for x number of files

                for num in range(1, len(self.args.multi_plot) + 1):
                    bq_coor_dict[f'bq_coors{num}'] = []
                    multi_plot_index[f'multi_plot_index{num}'] = self.args.multi_plot[num - 1]
                    iso_dict[f'isotrops{num}'] = []

                    for line in multi_plot_index[f'multi_plot_index{num}']:
                        if 'cBq' in line:
                            bq_coor_dict[f'bq_coors{num}'].append(float(line.split()[value]))
                        elif 'iBq' in line:
                            iso_dict[f'isotrops{num}'].append(float(line.split()[2]))
                # Append data to values in dicts as lists

                bq_coor_list = []
                iso_list = []

                for coor in bq_coor_dict.values():
                    bq_coor_list.append(coor)
                for iso in iso_dict.values():
                    iso_list.append(iso)  # Convert dicts to list of lists so they can be zipped with args

                nonrounded_x = [list(a) for a in zip(*bq_coor_list)]

                for i in nonrounded_x:
                    self.x_values.append([round(num, 3) for num in i])  # Round to 3 dp

                self.y_values = [list(b) for b in zip(*iso_list)]

        except (FileNotFoundError, ValueError, IndexError) as error:
            print('\nThere was an issue with reading the parsed data:')
            print(error)
            sys.exit()

        if self.args.verbose is True:
            print('x-axis:', *self.x_values, sep=' ')
            print('\ny-axis:', *self.y_values, sep=' ')

    def check_arrays(self):
        '''
        if self.x_values == [] and self.y_values == []:  # error catching
            print(f'\nError: {self.args.filename} is/are missing the lines containing cBq and iBq (ghost atom '
                  'coordinates and isotropic NICS values')
            sys.exit()
        elif self.x_values == []:
            print(f'\nError: {self.args.filename} is/are missing the lines containing cBq (ghost atom coordinates)')
            sys.exit()
        elif self.y_values == []:
            print(f'\nError: {self.args.filename} is/are missing the lines containing iBq (isotropic NICS values)')
            sys.exit()
        '''
        # TODO: implement the block comment above

        if self.args.shielding is True:
            self.y_axis_label = 'Isotropic Magnetic Shielding Tensor / ppm'
        elif not self.args.multi_plot:
            for chg_sign, num in enumerate(self.y_values):
                self.y_values[chg_sign] = num * -1
        else:
            for list in self.y_values:
                for chg_sign, num in enumerate(list):
                    list[chg_sign] = num * -1

    def draw_plot(self):
        try:
            x = self.x_values  # x-values; where the atoms are
            y = self.y_values  # The isotropic NICS values
            plt.plot(x, y)  # Plotting the points
            plt.xlabel('Distance from origin / \u212B', fontsize=16)
            plt.ylabel(self.y_axis_label, fontsize=16)
            plt.tick_params(axis='both', which='both', labelsize=12)
            # plt.title('Chemical Shift as a Function of Distance from the Origin Calculated Using NICS', fontsize=20)
            plt.show()

        except (ValueError, IndexError) as error:
            print('\nThere was an error with plotting the graph:')
            print(error)
    # TODO: Compare with 2D and update this script accordingly


if __name__ == '__main__':
    p = Plotter()
    p.cli_cmds()
    p.append_coors()
    p.check_arrays()
    p.draw_plot()
