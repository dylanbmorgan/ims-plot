
class input_generator:
    """
Easy way to add ghost atoms to end of Gaussian input (.com) file

Key (in alphabetical order): 
    'bq' = ghost atoms 
    'coor(s)' = coordinates 
    'func' = function
    'inp' = input
    'usr' = user
    'wf' = write file

Prerequisits:
    Molecule must already be aligned with origin
    (Optional) molecule geometry already optimised 
    Coors must be given by usr as float
    """

    def __init__(self):
        self.each_bq_coor = []

    def enter_bq_coor(self):
        """
        asks usr for coors for ghost atoms
        generates a list containing usr defined Bq coordinates
        prints list of coors 
        asks usr to confirm coors
        check() func allows usr to re-input coors or accept to add to inp file
        """

        print("\nEnter coordinates (x, y, z) for desired ghost atoms (separated by spaces).")
        print("Press 'enter' to enter next coordinate.")
        print("Press 'enter' again when finished:\n")

        each_coor = []
        # list to hold Bq coordinates 

        while True:
            coor = input()

            if coor != "":
                each_coor.append(coor)
            else:
                break

        self.each_bq_coor = ["Bq " + coor for coor in each_coor]
        # new list to enable adddition of "Bq"

        print("Output:")
        print(*self.each_bq_coor, sep = '\n')

        def check(): #TODO: remove increment
            cont = input("\nProceed? (y/n) ")

            if cont == "y" or cont == "yes":
                self.append_input_file()
            elif cont == "n" or cont == "no":
                self.enter_bq_coor()
            else:
                print("Not a valid answer.")
                check()

        check()


    def append_input_file(self):
        """
        asks usr for filename for original file name then asks for a name for a copy of the original file
        copys contents of original file to copy
        appends copied file with Bq atoms generated earlier
        adds new line to end of file to comply with Gaussian input file requirements
        opens copied file as read so usr can check it's been correctly generated 
        """

        original_filename = input("\nFile name:\n")
        copy_filename = input("\nName to save copy as:\n")

        with open(original_filename) as original:
            with open(copy_filename, "w+") as copy:

                for line in original:
                    copy.write(line)

                for coor in self.each_bq_coor:
                    copy.write('%s\n' % coor)

        with open(copy_filename, "r") as copy:

            if copy.mode == "r":
                contents = copy.read()
                print(contents)

        exit() # TODO: why


if __name__ == "__main__":
    ig = input_generator()
    print(ig.__doc__)
    #ig.preamble_func()
    ig.enter_bq_coor()
    ig.append_input_file() # TODO: twice ?