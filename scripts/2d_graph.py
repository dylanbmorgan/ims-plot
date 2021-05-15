#!/usr/bin/env python3
# 2d_graph_plotter.py
# Plots contour plot of isotropic NICS values from parsed file data
# Author: Dylan Morgan

import argparse
import glob
import matplotlib.pyplot as plt
import sys


class Plotter:

    def __init__(self):
        self.x_values = []
        self.y_values = []
        self.z_values = []
        self.rounded_x = []
        self.rounded_y = []
        self.z_axis_label = '\u03B4 / ppm'
        self.title = 'Chemical Shift Contour Plot Calculated using NICS'

    def cli_cmds(self):
        def formatter(prog):
            return argparse.HelpFormatter(prog, max_help_position=80)

        parser = argparse.ArgumentParser(formatter_class=formatter,
                                         description='Plots a contour plot to show isotropic NICS values from parsed'
                                         ' Gaussian log file data')
        parser.add_argument('-f', '--filename',
                            nargs='*',
                            default=glob.glob('parsed_data*.txt'),
                            # ^^ Might not work if a different file is specified other than default
                            help='if a custom file name was given for the parsed log data, use this flag to '
                            'specify the name of that file')
        parser.add_argument('-l', '--levels',
                            nargs='?',
                            type=int,
                            help='Specify the total number of contours in the final plot')
        parser.add_argument('-s', '--shielding',
                            action='store_true',
                            help='plot graph as a function of isotropic magnetic shielding instead of chemical shift')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='print the values of the x and y axes of the plot')

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
                            self.rounded_x = [round(num, 3) for num in self.x_values]
                            self.y_values.append(float(words[axis_y]))  # Bq coors
                            self.rounded_y = [round(num, 3) for num in self.y_values]

                        elif 'iBq' in line:
                            self.z_values.append(float(words[2]))  # isotropic values

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
            self.z_axis_label = 'Isotropic Magnetic Shielding Tensor'
            self.title = 'Isotropic NICS Contour Plot'
        else:
            for chg_sign, num in enumerate(self.z_values):
                self.z_values[chg_sign] = num * -1

    def draw_plot(self):
        if self.args.verbose is True:
            self.rounded_x.insert(0, 'x-values')
            self.rounded_y.insert(0, 'y-values')
            self.z_values.insert(0, 'z-values')

            for x, y, z in zip(self.rounded_x, self.rounded_y, self.z_values):
                print(x, y, z)  # Prints arrays as columns

            del self.rounded_x[0]
            del self.rounded_y[0]
            del self.z_values[0]

        x = self.rounded_x
        y = self.rounded_y
        z = self.z_values

        try:
            # data
            fig, ax = plt.subplots()

            if self.args.levels is not None:
                cp = ax.tricontourf(x, y, z, levels=self.args.levels)
            else:
                cp = ax.tricontourf(x, y, z)

            # labels
            cbar = fig.colorbar(cp)
            cbar.set_label(self.z_axis_label, fontsize=14)
            # ax.clabel(cp, inline=True, manual=False, fmt='%1.1f', fontsize=8)

            # I think there is a bug with matplotlib, where if clabel is used with a filled tricontour (tricontourf),
            # it messes up the rest of the plot. Uncomment the ax.clabel line to see what I mean.

            # axes and title
            ax.set_xlabel('Distance from x-origin / \u00c5', fontsize=16)
            ax.set_ylabel('Distance from y-origin / \u00c5', fontsize=16)
            ax.set_title(self.title, fontsize=20)
            ax.tick_params(labelsize=12)

            # print
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
