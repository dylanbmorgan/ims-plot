
def preamble_func():

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

def enter_bq_coor():
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

    each_bq_coor = ["Bq " + coor for coor in each_coor]

    print(*each_bq_coor, sep = '\n')

    def check():
        cont = input("\nProceed (y/n)? ".lower())

        if cont == "y" or cont == "yes":
            append_input_file()
        elif cont == "n" or cont == "no":
            enter_bq_coor()
        else:
            print("Not a valid answer.")
            check()
    
    check()

def append_input_file():
    """
    usr defines inp file to open
    func writes previously generated coors to inp file
    """

    file_name = input("\nFile name:\n")

    wf = open(file_name, "w")

    for line in open(file_name, "r"):
        wf.write(line)
    
    """
    for istep in range(nsteps):
        coor = start_vec + istep * inc_vec
"""

if __name__ == "__main__":
    preamble_func()
    enter_bq_coor()
    append_input_file()