#!/usr/bin/python

import matplotlib.pyplot as plt  


class plotter:

    def __init__(self):
        self.xvalues = []
        self.yvalues = []
        self.zvalues = []

    def append_coors(self):
        axisa = None
        axisb = None
        xinput = input('\nIn which plane do the coordinates change? (xy, xz, or yz): ')
        print('')

        if xinput == 'xy':
            axisa = 2
            axusb = 3
        elif xinput == 'xz':
            axisa = 2
            axisb = 4
        elif xinput == 'yz':
            axisa = 3
            axisb = 4
        else:
            print('Not a valid option, please pick again.\n')
            p.append_coors()

        with open('parsed_log_data') as data:
            for line in data:
                words = line.split()

                if 'cBq' in line:
                    self.xvalues.append(float(words[axisa]))
                    self.zvalues.append(float(words[axisb]))
                elif 'iBq' in line:
                    self.yvalues.append(float(words[2]))

        print('x-axis:', *self.xvalues, sep = ' ')
        print('y-axis:', *self.yvalues, sep = ' ')

    def create_plot(self):    
        x = self.xvalues  #x-values: where the atoms are for axisa
        y = self.yvalues  #the isotropic NICS values
        z = self.zvalues  #x-values: where the atoms are for axisb
        plt.plot(x, y, z)  #plotting the points   
        plt.show()  #function to show the plot  

if __name__ == '__main__':
    p = plotter()
    p.append_coors()
    p.create_plot()
