#!/usr/bin/env python3
# 1d_graph_plotter.py
# Plots graph of isotropic NICS values from parsed data file
# Author: Dylan Morgan

import matplotlib.pyplot as plt
import argparse
import sys


class Plotter:

    def __init__(self):
        self.xvalues = []
        self.yvalues = []

    def cli_cmds(self):
        self.parser = argparse.ArgumentParser(description='Plots a graph to show isotropic NICS values from parsed '
                                              'Gaussian log file data')
        self.axis_group = self.parser.add_mutually_exclusive_group(required=True)

        self.axis_group.add_argument('-x', '--xaxis',
                                     action='store_true',
                                     help='specify the direction the ghost atoms are plotted in as the x-axis')
        self.axis_group.add_argument('-y', '--yaxis',
                                     action='store_true',
                                     help='specify the direction the ghost atoms are plotted in as the y-axis')
        self.axis_group.add_argument('-z', '--zaxis',
                                     action='store_true',
                                     help='specify the direction the ghost atoms are plotted in as the z-axis')

        self.parser.add_argument('-f', '--file',
                                 action='store_true',
                                 default='.parsed_log_data.txt',
                                 help='if a custom file name was given for the parsed log data, use this flag to '
                                 'specify the name of that file')

        self.args = self.parser.parse_args()

    def append_coors(self):
        if self.args.xaxis is True:
            value = 3
        elif self.args.yaxis is True:
            value = 4
        elif self.args.zaxis is True:
            value = 5

        try:
            with open(self.args.file) as data:
                for line in data:
                    words = line.split()

                    if 'cBq' in line:
                        self.xvalues.append(float(words[value]))
                    elif 'iBq' in line:
                        self.yvalues.append(float(words[2]))

                if 'cBq' and 'iBq' not in data:
                    print('\nError: cBq and iBq not found in parsed log data')
                    sys.exit()
                elif 'cBq' not in data:
                    print('\nError: cBq not found in parsed log data')
                    sys.exit()
                elif 'iBq' not in data:
                    print('\nError: iBq not found in parsed log data')
                    sys.exit()

        except (FileNotFoundError) as error:
            print('\nThere was an issue with reading the parsed data:')
            print(error)

        print('x-axis:', *self.xvalues, sep=' ')
        print('y-axis:', *self.yvalues, sep=' ')

    def create_plot(self):
        try:
            x = self.xvalues  # x-values; where the atoms are
            y = self.yvalues  # The isotropic NICS values
            plt.plot(x, y)  # Plotting the points
            plt.show()  # Function to show the plot

        except (IndexError, ValueError) as error:
            print('\nThere was an error in plotting the graph:')
            print(error)


if __name__ == '__main__':
    pl = Plotter()
    pl.cli_cmds()
    pl.append_coors()
    pl.create_plot()