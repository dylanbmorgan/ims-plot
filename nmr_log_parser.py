
class log_parser:
    """
Takes .log output file from Guassian 
Reads isotropic NICS values 
Prints to new file
    """

    def __init__(self):
        self.iso_values = []

    def read_file(self):

        filename = input("Gaussian output file name (must be full path): ")
        log_line = []

        with open(filename) as log_file:
            for line in log_file:
                if "Isotropic" in line and "Bq" in line:
                    log_line.append(line.split())
                        
            for line in log_line:
                for word in line:
                    if word == line[4]:
                        self.iso_values.append(float(word))

            #trying to append only the 4th item in line to iso_value

            print(self.iso_values)
                       
        #print all iso values 
            
    def copy_iso_values(self):
        #copy isotropic values to new file
        pass

if __name__ == "__main__":
    lp = log_parser()
    print(lp.__doc__)
    lp.read_file()
    