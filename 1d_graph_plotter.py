
import matplotlib.pyplot as plt  


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
                words = line.split()
                if 'cBq' in line:
                    self.xvalues.append(float(words[axis]))
                elif 'iBq' in line:
                    self.yvalues.append(float(words[2]))

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