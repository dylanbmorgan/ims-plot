"""
Generates ghost atoms for NICS calculations of aromatic compounds for Gaussian 

Prerequisits:
    Molecule must be aligned with z-plane 
"""


import numpy as np


def input_params():
    """
    asks usr for input file name and ghost atom parameters (start, end, spacings)
    generates list of z coordinates for GAs
    appends list with x and y coordinates 
    """

    file_name = input("Type the name of the input file to be appended: ")

    ga_no_start = int(input("What is the start coordinate for the GAs? "))
    ga_no_end = int(input("What is the end coordinate for the GAs? "))
    ga_spacing = float(input("What are the vecotr spacings between GAs? "))

    ga_list = np.arange(ga_no_start, ga_no_end + ga_spacing, ga_spacing).tolist()

    return file_name, ga_list

        

def append_input_file(file_name, ga_list):
    """
    appends the Gaussian input file with ghost atoms
    checks to see if file is empty
    iterate over each string in a list
    if not empty, will add input as new line
    other lines will append new line at the end of preceding line

    modified from: https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/ (accessed 06/11/2020)
    """

    with open(file_name, "a+") as file_object:
        append_eol = False

        file_object.seek(0)
        data = file_object.read(100)

        if len(data) > 0:
            append_eol = True

        for line in lines_to_append:
            if append_eol == True:
                file_object.write("/n") 

            else:
                append_eol = True

            file_object.write(line)


if __name__ == "__main__":
    input_params()
    append_input_file()