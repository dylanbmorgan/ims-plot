
def felix_code():
    """So, the print-out would be something along the lines of"""

      print("Bq  % 12.6f % 12.6f % 12.6f"%(x, y, z))
    
    """This means that you are formatting float numbers: 12 digits in total, 6 decimal digits"""

    """And, in the long run, the coordinates would be vectors. So, you would do somthing along the lines"""

        tmp = input("Enter the coordinates (x, y, z) for the first ghost atom (separated by spaces)")

        start_list = [float(coor) for coor in tmp.split()]

        # or if you want to use numpy

        start_vec = numpy.array(tmp.split(), float)


def append_input_file_v2():
    """
    Open inp file
    write atomic coordinates to new file
    """

    wf = open(file_name, "w")

    for line in open(file_name, "r"):
        wf.write(line)
    
    for istep in range(nsteps):
        # coor = start_vec + istep * inc_vec