
class input_generator:

    def preamble_func(self):

        preamble = """
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
        """

        print(preamble)


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

        def check():
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
        assigns enter_bq_coor() to each_bq_coor variable
        usr defines inp file to open
        func writes previously generated coors to inp file
        func add new line to end of file (to comply with Gaussian requiring blank empty line at end of file)
        prints content of modified file
        """

        file_name = input("\nFile name:\n")

        with open(file_name, 'w') as gaus_file:

            for coor in self.each_bq_coor:
                gaus_file.write('%s\n' % coor)

            gaus_file.write('\n')
            #print(gaus_file.read())


if __name__ == "__main__":
    ig = input_generator()
    ig.preamble_func()
    ig.enter_bq_coor()
    #ig.append_input_file()