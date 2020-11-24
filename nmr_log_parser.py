
class log_parser:
    """
Takes .log output file from Guassian 
Reads isotropic NICS values 
Prints to new file
    """

    def __init__(self):
        self.each_log_line = []
        self.bq_iso_value = []

    def read_file(self):

        filename = input("Gaussian output file name (must be full path): ")

        with open(filename) as log_file:
            for line in log_file:
                if "Isotropic" in line and "Bq" in line:
                    
                    #iso_line = line.split()

                    #iso_value = #4th item in 

                    #for 4th value in line, add value to bq_iso_value 
                    #try in while loop?*
                    #try with numpy array maybe?
                    #try adding contents of line as a list and adding fourth item in list to new list?
                       
        #print all iso values 
            
    def copy_iso_values(self):
        #copy isotropic values to new file
        pass

if __name__ == "__main__":
    lp = log_parser()
    print(lp.__doc__)
    lp.read_file()


# *something like:
#
# while length of list <2:
#   skip line 
# else:
#   add item in line to list 