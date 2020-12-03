
class log_parser:
    '''
Takes .log output file from Guassian 
Reads isotropic NICS values 
Prints to new file

Glossary (in alphabetical order):
    'coors' = coordinates 
    'iso' = isotropic NICS values
    '''

    def __init__(self):
        self.filename = None
        self.iso_values = []
        self.all_lines = []
        self.coors = []

    def read_iso_values(self):
        self.filename = input('Gaussian output file name (must be full path): ')
        logline = []

        with open(self.filename) as logfile:
            for line in logfile:
                if 'Isotropic' in line and 'Bq' in line:
                    logline.append(line.split())
                        
            for line in logline:
                for word in line:
                    if word == line[4]:
                        self.iso_values.append(float(word))

            print(*self.iso_values, sep = '\n')

    def read_coors(self):
        with open(self.filename) as logfile:
            for line in logfile:
                self.all_lines.append(line)

            for line in self.all_lines:
                if 'Isotropic' in line:
                    line = next(logfile)
                    self.coors.append(line)

                    #trying to select the line after the line which contains the strings 'Isotropic' and 'Bq'

    def copy_iso_values(self):
        '''
        copy iso values and coors to new file
        '''

        copy_filename = input('Name to save data as (must be full path):')

        with open(copy_filename, 'w+') as copy:
            copy.write('\nNICS Isotropic Values:')
            
            for line in self.iso_values:
                copy.write(line)

            copy.write('\nGhost Atom Matrix Coordinates:')

            for line in self.coors:
                copy.write(line)
        
        with open(copy_filename, 'r') as copy:
            contents = copy.read()
            print(contents)


if __name__ == '__main__':
    lp = log_parser()
    print(lp.__doc__)
    lp.read_iso_values()
    lp.read_coors()
    lp.copy_iso_values()


'''  
TODO:
[] Enable parsing of matrix coors to lists
[] Print iso values as column
[] Copy lists to new file
'''

'''
NOTE:
/home/dylanmorgan/python/test/nmr_anthracene.log

def read_iso_value(self):
    #possible alt to other func with same name

    filename = input('Gaussian output file name (must be full path): ')
    all_lines = []
    logline = []
    
    with open(filename) as logfile:
        for line in logfile:
            logline.append(line.split())

            if 'Isotropic' in line and 'Bq' in line:
                logline.append(line)
                print logline
'''