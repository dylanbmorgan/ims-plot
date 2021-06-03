#!/usr/bin/env python3
# 2d_graph_plotter.py
# Plots contour plot of isotropic NICS values from parsed file data
# Authors: Dylan Morgan & Dr Felix Plasser

import argparse
# import glob
import matplotlib.pyplot as plt
import numpy as np
import sys


class Plotter:

    def __init__(self):
        self.x_coors = []
        self.y_coors = []
        self.nics_vals = []

    def cli_cmds(self):
        def formatter(prog):
            return argparse.HelpFormatter(prog, max_help_position=80)

        parser = argparse.ArgumentParser(formatter_class=formatter,
                                         description='Plots a contour plot to show isotropic NICS values from parsed'
                                         ' Gaussian log file data')
        parser.add_argument('-c', '--colours',
                            action='store_true',
                            help='use an alternative colourscheme for the IMS plot')
        parser.add_argument('-f', '--filename',
                            # default=glob.glob('parsed_data*.txt'),
                            nargs='+',
                            type=argparse.FileType('r'),
                            help='if a custom file name was given for the parsed log data, use this flag to '
                            'specify the name of that file')
        parser.add_argument('-i', '--interactive',
                            action='store_true',
                            help='open an interactive version of the generated IMS plot')
        parser.add_argument('-l', '--levels',
                            nargs='?',
                            type=int,
                            help='specify the total number of contours in the final plot')
        parser.add_argument('-p', '--plot_name',
                            default='IMS_plot.png',
                            nargs='?',
                            help='give a custom name when saving the IMS plot')
        parser.add_argument('-r', '--range',
                            action='store_true',
                            help='specify a custom maximum and minimum \u03B4 value')
        parser.add_argument('-s', '--shielding',
                            action='store_true',
                            help='plot graph as a function of isotropic magnetic shielding instead of chemical shift')
        parser.add_argument('-t', '--title',
                            nargs='?',
                            help='assign a title to the IMS plot')
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
            # sys.path.append('./')
            # import input_data as inp  # type: ignore
            # Also have to change file extension from a txt to py

            # x_vals = [round(inp.min_x + i * inp.step_x, 5) for i in range(inp.dim_x)]
            # y_vals = [round(inp.min_y + i * inp.step_y, 5) for i in range(inp.dim_y)]
            # self.nics_vals = np.zeros([inp.dim_x, inp.dim_y], float)

            # Alternative (maybe better?) way of doing it ^^

            inp_dict = {}

            with open('input_data.txt', 'r') as inp:
                for line in inp:
                    word = line.split()
                    inp_dict[word[0]] = float(word[2])

            self.x_coors = [round(inp_dict['min_x'] + i * inp_dict['step_x'], 5) for i in range(int(inp_dict['dim_x']))]
            self.y_coors = [round(inp_dict['min_y'] + i * inp_dict['step_y'], 5) for i in range(int(inp_dict['dim_y']))]
            self.nics_vals = np.zeros([int(inp_dict['dim_x']), int(inp_dict['dim_y'])], float)
            # TODO: fix for if x and y are different lengths

            for file in self.args.filename:
                x_tmp = []
                y_tmp = []
                nics_tmp = []

                for line in file:
                    words = line.split()
                    if 'cBq' in line:
                        x_tmp.append(float(words[axis_x]))
                        y_tmp.append(float(words[axis_y]))  # Put data from file into temp arrays
                    elif 'iBq' in line:
                        nics_tmp.append(float(words[2]))

                # Put data into the global array at an appropriate position
                for i, val in enumerate(nics_tmp):
                    x_vals = round(x_tmp[i], 5)
                    y_vals = round(y_tmp[i], 5)  # Round to 5 dp

                    ix = self.x_coors.index(x_vals)
                    iy = self.y_coors.index(y_vals)
                    self.nics_vals[ix, iy] = val

        except (FileNotFoundError, ValueError, IndexError) as error:
            print('\nThere was an issue with reading the parsed data:')
            print(error)
            sys.exit()

    def check_arrays(self):
        if self.x_coors is None and self.nics_vals is None:
            print(f'\nError: {self.args.filename} are missing the lines containing cBq and iBq (ghost atom '
                  'coordinates and isotropic NICS values)')
            sys.exit()
        elif self.x_coors is None or self.y_coors is None:
            print(f'\nError: {self.args.filename} are missing the lines containing cBq (ghost atom coordinates)')
            sys.exit()
        elif self.nics_vals is None:
            print(f'\nError: {self.args.filename} are missing the lines containing iBq (isotropic NICS values)')
            sys.exit()

    def draw_plot(self):
        if self.args.shielding is True:
            cb_label = 'Isotropic Magnetic Shielding'  # Change axis label for shielding
        else:
            cb_label = '\u03B4 / ppm'
            for chg_sign, num in enumerate(self.nics_vals):
                self.nics_vals[chg_sign] = num * -1  # Flip IMS sign to get to chemical shift

        if self.args.verbose is True:
            print(f'\nx coordinates:\n{self.x_coors}')
            print(f'\ny coordinates:\n{self.y_coors}')
            print(f'\nNICS isotropic values:\n{self.nics_vals}')

        x = self.x_coors
        y = self.y_coors
        z = self.nics_vals

        try:
            if self.args.range is True:
                min = int(input('\nInput the minimum value for \u03B4 (must be an integer): '))
                max = int(input('Input the maximum value for \u03B4 (must be an integer): '))
            else:
                min = -20
                max = 20

            # Data
            fig, ax = plt.subplots()

            if self.args.colours is True:  # Different plot colours
                map = plt.get_cmap('viridis')
            else:
                map = plt.get_cmap('RdBu')

            if self.args.levels is not None:  # Change no. of contours
                cp = ax.contourf(x, y, z, levels=self.args.levels, vmin=min, vmax=max, cmap=map)
            else:
                cp = ax.contourf(x, y, z, vmin=min, vmax=max, cmap=map)

            # Labels
            cbar = fig.colorbar(cp)
            cbar.set_label(cb_label, fontsize=14)
            # ax.clabel(cp, inline=True, manual=False, fmt='%1.1f', fontsize=8)

            # I think there is a bug with matplotlib, where if clabel is used with contourf,
            # it messes up the rest of the plot. Uncomment the ax.clabel line to see what I mean.
            # It works with contour though

            # Axes and title
            ax.set_xlabel('Distance from x-origin / \u00c5', fontsize=14)
            ax.set_ylabel('Distance from y-origin / \u00c5', fontsize=14)
            ax.tick_params(labelsize=12)
            if self.args.title is not None:
                ax.set_title(self.args.title, fontsize=16)

            # Print
            if self.args.interactive is True:
                plt.show()
            else:
                plt.savefig(self.args.plot_name)

        except (ValueError, IndexError, TypeError) as error:
            print('\nThere was an error with plotting the graph:')
            print(error)


if __name__ == '__main__':
    p = Plotter()
    p.cli_cmds()
    p.append_coors()
    p.check_arrays()
    p.draw_plot()
