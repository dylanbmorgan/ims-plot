
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

    def read_coors(self):
        with open(self.filename) as logfile:
            while True:
                try:
                    line = next(logfile)
                    if 'Isotropic' in line and 'Bq' in line:
                        line = next(logfile)
                        self.coors.append(line)
                        line = next(logfile)
                        self.coors.append(line)
                        line = next(logfile)
                        self.coors.append(line)

                except StopIteration:
                    break
            
        print(f'\nFinished parsing file {self.filename}\n')

    def copy_iso_values(self):
        '''
        copy iso values and coors to new file
        append Bq and count to each line
        '''

        copy_filename = input('Name to save data as must be full path: ')

        with open(copy_filename, 'w+') as copy:
            copy.write('\nNICS Isotropic Values:\n')
            for count, line in enumerate(self.iso_values, 1):
                copy.write(str(f'{count}  Bq:  {line}\n'))

            copy.write('\nGhost Atom Coordinates:\n')
            for line in self.coors:   
                if 'XZ' in line:
                    copy.write(f'{line}\n')
                else:
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
[X] Print iso values as column
[X] Copy lists to new file
[X] Make read_coors() work
[X] Make read_coors work() for other coors (and not just X) 
[ ] Fix spacings between coors so there are no spaces between XX, XY, XZ and 1 between each Bq
    # Maybe can use: 
    # for n in range:
    # from inp_gen_1d
[ ] Print each Bq atom with its label (eg. 4 Bq [then coors here])


NOTE:
pop:
/home/dylanmorgan/python/test/nmr_anthracene.log
/home/dylanmorgan/python/test/parsed_nmr_anthracene.txt

manjaro:
/home/pop!_os/home/dylanmorgan/python/test/nmr_anthracene.log
/home/pop!_os/home/dylanmorgan/python/test/parsed_nmr_anthracene.txt
'''