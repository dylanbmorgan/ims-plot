
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
        self.inp_filename = None
        self.out_filename = None
        self.coors = []
        self.iso_values = []
        self.tensors = []

    def read_coors(self):
        self.inp_filename = input('Gaussian input file name (must be full path): ')

        with open(self.inp_filename) as comfile:
            for line in comfile:
                if 'Bq' in line:
                    self.coors.append(line)

    def read_iso_values(self):
        self.out_filename = input('Gaussian output file name (must be full path): ')
        logline = []

        with open(self.out_filename) as logfile:
            for line in logfile:
                if 'Isotropic' in line and 'Bq' in line:
                    logline.append(line.split())
                        
            for line in logline:
                for word in line:
                    if word == line[4]:
                        self.iso_values.append(float(word))

    def read_tensors(self):
        with open(self.out_filename) as logfile:
            while True:
                try:
                    line = next(logfile)
                    if 'Isotropic' in line and 'Bq' in line:
                        line = next(logfile)
                        self.tensors.append(line)
                        line = next(logfile)
                        self.tensors.append(line)
                        line = next(logfile)
                        self.tensors.append(line)

                except StopIteration:
                    break
            
        print(f'\nFinished parsing file: {self.out_filename}\n')

    def copy_iso_values(self):
        '''
        copy coors, iso values, and tensors to new file
        append Bq and count to each line
        '''

        copy_out_filename = input('Name to save data as (must be full path): ')

        with open(copy_out_filename, 'w+') as copy:
            copy.write('\nGhost Atom Coordinates:\n')
            for count, line in enumerate(self.coors, 1):
                copy.write(str(f'{count} {line}'))

            copy.write('\n\nNICS Isotropic Values:\n')
            for count, line in enumerate(self.iso_values, 1):
                copy.write(str(f'{count}  Bq:  {line}\n'))

            copy.write('\nGhost Atom Tensors:\n')
            for line in self.tensors:   
                if 'XZ' in line:
                    copy.write(f'{line}\n')
                else:
                    copy.write(line)
        
        with open(copy_out_filename, 'r') as copy:
            contents = copy.read()
            print(contents)


if __name__ == '__main__':
    lp = log_parser()
    print(lp.__doc__)
    lp.read_coors()
    lp.read_iso_values()
    lp.read_tensors()
    lp.copy_iso_values()


'''  
TODO:
[X] Print iso values as column
[X] Copy lists to new file
[X] Make read_tensors() work
[X] Make read_tensors work() for other tensors (and not just X) 
[(x)] Fix spacings between tensors so there are no spaces between XX, XY, XZ and 1 between each Bq
    # Maybe can use: 
    # for n in range:
    # from inp_gen_1d
[N/A] Print each Bq atom with its label (eg. 4 Bq [then tensors here])
[ ] Fix example files. Benzene is given as input and anthracene is given as output


NOTE:
pop:
/home/dylanmorgan/python/test/nmr_anthracene.log
/home/dylanmorgan/python/test/parsed_nmr_anthracene.txt

manjaro:
/home/pop!_os/home/dylanmorgan/python/test/benzene_opt_target.com
/home/pop!_os/home/dylanmorgan/python/test/nmr_anthracene.log
/home/pop!_os/home/dylanmorgan/python/test/parsed_nmr_anthracene.txt
'''