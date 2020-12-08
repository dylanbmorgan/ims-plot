
import matplotlib.pyplot as plt  
import numpy as np


class plotter:

    def __init__(self):
        self.xvalues = []
        self.yvalues = []

    def append_coors(self):
        axis = None
        xinput = input('\nAxis which coordinates change (x, y, or z): ')
        print('')

        if xinput == 'x':
            axis = 2
        elif xinput == 'y':
            axis = 3
        elif xinput == 'z':
            axis = 4
        else:
            print('Not a valid option, please pick again.\n')
            p.append_coors()

        xcoor_line = []
        ycoor_line = []

        with open('parsed_log_data') as data:
            for line in data:
                if 'cBq' in line:
                    xcoor_line.append(line.split())
                elif 'iBq' in line:
                    ycoor_line.append(line.split())

            for line in ycoor_line:
                for word in line:
                    if word == line[2]:
                        self.yvalues.append(float(word))
            
            for line in xcoor_line:
                for word in line:
                    if word == line[axis] and word != '0.0':
                        self.xvalues.append(float(word))
                    elif word == '0.0' and word != '10.0' and word == line[axis]:
                        zero = len(xcoor_line)/2

                        if zero % 2 == '0':
                            self.xvalues.insert(int(zero), '0.0')
                        elif zero % 2 != '0':
                            zero_odd = zero + 0.5 
                            self.xvalues.insert(int(zero_odd), '0.0')

                        # If 0.0 is not excluded, will add >1 0.0 value to xvalues list.
                        # Only occurs if there is a 0.0 value in ghost atom coordinates.
                        # As a workaround, exclude 0.0 from being added to the list, 
                        # and divide length of list by 2.
                        # Add 0.0 to this point in the list 

        print('x-axis:', *self.xvalues, sep = ' ')  #remove when committing 
        print('y-axis:', *self.yvalues, sep = ' ')  #remove when committing 

    def create_plot(self):    
        x = self.xvalues  #x-values; where the atoms are   
        y = self.yvalues  #the isotropic NICS values
        plt.plot(x, y)  #plotting the points   
        plt.show()  #function to show the plot  

if __name__ == '__main__':
    p = plotter()
    p.append_coors()
    p.create_plot()


'''
TODO: 
[ ] Prevent multiple 0.0 values from being added to xvalues list
'''