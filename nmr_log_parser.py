
class log_parser:
    """
Takes .log output file from Guassian 
Reads isotropic NICS values 
Prints to new file
    """

    def __init__(self):
        self.filename = None
        self.iso_values = []
        self.xx_coors = []
        self.xy_coors = []
        self.xz_coors = []

    def read_iso_value(self):
        self.filename = input("Gaussian output file name (must be full path): ")
        logline = []

        with open(self.filename) as logfile:
            for line in logfile:
                if "Isotropic" in line and "Bq" in line:
                    logline.append(line.split())
                        
            for line in logline:
                for word in line:
                    if word == line[4]:
                        self.iso_values.append(float(word))

            print(self.iso_values)

    def read_xx_line(self):
#        all_lines = []
#        xxline = []
        
#        with open(self.filename) as logfile:
#            for line in logfile:
#                all_lines.append(line.split())

#        for line in all_lines:
#            if "Bq" and "Isotropic" in line:
#                xxline.append(line)

#        with open(self.filename) as original:
#            with open("log_copy.txt", "w+") as copy:
#                for line in original:
#                    copy.write(line)
                    
#                for line in copy:
#                    if "Bq" and "Isotropic" in line:
#                        copy.write("")

    def copy_iso_values(self):
        #copy isotropic values and coors to new file
        pass

if __name__ == "__main__":
    lp = log_parser()
    print(lp.__doc__)
    lp.read_iso_value()
    lp.read_xx_line()
    


"""
def read_iso_value(self):
    #possible alt to other func with same name

    filename = input("Gaussian output file name (must be full path): ")
    all_lines = []
    logline = []
    
    with open(filename) as logfile:
        for line in logfile:
            logline.append(line.split())

            if "Isotropic" in line and "Bq" in line:
                logline.append(line)
                print logline
"""