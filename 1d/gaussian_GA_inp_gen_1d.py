
import numpy


class input_generator:
    """
Easy way to add ghost atoms to end of Gaussian input (.com) file

Glossary (in alphabetical order):
    'bq' = ghost atoms
    'coor(s)' = coordinates
    'func' = function
    'inp' = input
    'usr' = user
    'vs' = vector spacings
    'wf' = write file

Important Notes:
    Molecule must already be aligned with origin
    (Optional) molecule geometry already optimised
    Only coors from one dimension should be changed
    """

    def __init__(self):
        self.bq_coors = []
        # class-assigned list where bq atoms will be appended to
        # alternative to using global variable

    def enter_bq_coor(self):
        """
        asks usr for coor of first bq, vs, and no of bq atoms
        generates a array of coors accordingly
        prints list of coors
        asks usr to confirm coors
        check() func allows usr to re-input coors or accept to append to copied inp file
        """

        coor = input("\nEnter coordinates (x, y, z) for first ghost atom separated by spaces: ")
        vs = input("Specify vector spacings (x, y, z) separated by spaces: ")
        bq_no = int(input("Specify number of ghost atoms: "))

        print("\n")
        print("Output:\n")

        x0 = numpy.array(coor.split(), float)
        delta_xyz = numpy.array(vs.split(), float)

        for n in range(bq_no):
            xn = x0 + n * delta_xyz
            self.bq_coors.append(f"Bq {xn[0]} {xn[1]} {xn[2]}")
        
        print(*self.bq_coors, sep = '\n')  
            
        # TODO: [x] prevent from iterating over x and y coors 
        #       [x] pass to variable or list instead of printing
        #       [x] assign variable or list as class so will be able to move between functions
        #       [x] update variables in append_inp_file()
        #       [x] create list for coors
        #       [x] (optional) replace % string format with f string for self.bq_coors
        #       [ ] (optional) change % for f string in append_inp_file()
        #       [ ] (optional) prevent usr from entering any values incorrectly (eg. vs) by creating loop allowing them to re-enter

    def check(self):
        cont = input("\nProceed? (y/n) ")

        if cont.lower() == "y" or cont.lower() == "yes":
            self.append_inp_file()
        elif cont.lower() == "n" or cont.lower() == "no":
            self.enter_bq_coor()
            ig.check()
        else:
            print("Not a valid answer.")
            ig.check()

    def append_inp_file(self):
        """
        asks usr for original filename then asks for name for copy of original file
        copys contents of original file to copy
        appends copied file with Bq atoms generated earlier
        adds new line to end of file to comply with Gaussian input file requirements
        opens copied file as read so usr can check it's been correctly generated
        """

        original_filename = input("\nFile to copy (must be full path):\n")
        copy_filename = input("\nName to save copy as (must be full path):\n")

        with open(original_filename) as original:
            with open(copy_filename, "w+") as copy:

                for line in original:
                    copy.write(line)

                for coor in self.bq_coors:
                    copy.write(f'{coor}\n')

        with open(copy_filename, "r") as copy:

            if copy.mode == "r":
                contents = copy.read()
                print(contents)


if __name__ == "__main__":
    ig = input_generator()
    print(ig.__doc__)
    ig.enter_bq_coor()
    ig.check()
    ig.append_inp_file()
