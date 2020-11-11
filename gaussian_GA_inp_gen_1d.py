
def preamble_func():

    preamble = """
    Generates ghost atoms for NICS calculations of aromatic compounds for Gaussian 

    Key (in order of appearance):
        Bq = ghost atoms 
        coor = coordinates 

    Prerequisits:
        Molecule must be aligned with origin
    """

    print(preamble)


import numpy as np


def enter_Bq_coor():

    print("Enter coordinates (x, y, z) for desired ghost atoms (without any separation between coordinates)")
    print("Press 'enter' to enter next coordinate")
    print("Press 'f + enter' when finished:")

    ga_coor_list = []

    while True:
        ga_coor = input()

        if ga_coor != "f":
            ga_coor_list.append(float(ga_coor))

        else:
            break    

    print(ga_coor_list)

"""
    def check():

        cont = input("Proceed (y/n)? ".lower())

        if cont == y:
            append_input_file_v2()
        
        elif cont == n:
            enter_Bq_coor()

        else:
            print("Not a valid answer.")
            check()
"""

if __name__ == "__main__":
    preamble_func()
    enter_Bq_coor()
    #append_input_file_v2()