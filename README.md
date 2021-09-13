# IMS-plot

For literature on the topic, here is a [review](https://github.com/dylanbmorgan/ims-plot/blob/main/literature/lit_review.pdf)

For a journal-style report on the use of ims-plot, see [here](https://github.com/dylanbmorgan/ims-plot/blob/main/literature/final_report.pdf)

## ATTENTION
I am not currently developing this any further. This may change in the future 
but I feel like this is unlikely as my time will be spend working on my PhD. If 
you happen to stumble accross this and have any questions about its use, feel 
free to drop me an email and I will be happy to assist. 

Dylan 

## Prerequisites & Dependencies

These instructions assume basic knowledge of the unix command line. For an
excellent tutorial of the command line, I would personally recommend [Ryans
Tutorials](https://ryanstutorials.net/linuxtutorial/).

They are intended to be used with the Gaussian09 software. They have not been 
tested on other Gaussian versions, however there should be 
compatibility between versions. These scripts will not work with other quantum 
chemistry software. 

Additionally, this repository has only been tested on a system using the linux
kernel. As it is exclusively written in python and bash, it should also work on
MacOS, although the `$PATH` variables may differ slightly. It has not been
tested on windows systems.

## Installation

This is currently a simple collection of scripts, however will likely become a
fully installable program in future versions...

I would advise creating a directory in your `$HOME` to execute the scripts from
and to add this directory to your `$PATH`. To do so, paste the following into
your terminal:

```sh
cd ~/
git clone https://github.com/dylanbmorgan/ims-plot.git ~/bin/ims-plot
```

To add the directory to your `$PATH`:

If you are using bash:

```sh
echo 'export PATH=$HOME/bin/ims-plot/scripts:$PATH' >> ~/.bash_profile
source ~/.bash_profile
```

For zsh users:

```sh
echo 'export PATH=$HOME/bin/ims-plot/scripts:$PATH' >> ~/.zshrc
source ~/.zshrc
```

For fish users:

```sh
echo 'export PATH="$HOME/bin/ims-plot/scripts:$PATH"' >> ~/.config/fish/config.fish
source ~/.config/fish/config.fish
```

If you are unsure which shell you are using, you can find out by executing the
following:

```sh
echo $SHELL
```

## Usage

The following applies to the usage of all the scripts:

1. Use a molecular editor (such as [JMol](http://jmol.sourceforge.net/),
   [Avogadro](https://www.openchemistry.org/projects/avogadro2/), etc.) to draw a
   rough structure of the molecule in question.
1. Use force-field methods to pre-optimise the structure,
   * The editor's in-built methods are more than sufficient for this.
1. Optimise the structure in Gaussian.
    * It is recommended to use a functional and basis set at least as accurate
     as PBE0/Def2-SVP for this.
        * This hybrid functional and split-valence polarised basis set should
        be accurate enough to appropriately describe most systems, whilst using
        more expensive levels of theory is not likely to significantly affect
        the optimised structure.
        * All examples given here have been calculated using this level of
        theory.
    * In the Gaussian input file, this can be written as follows:
        * `# PBE1PBE/Def2SVP opt`
1. Parse the information from the Gaussian output file to a new input file.
    * It is recommended to employ [Open Babel](http://openbabel.org/wiki/Main_Page)
    for this.
1. Check that the structure has optimised correctly
1. Modify the new input file in the same way as the file used for the
   optimisation, with the exception of writing `nmr` rather than `opt`: 
    * `# PBE1PBE/Def2SVP nmr`
1. Ensure to ***remove*** the empty line at the end of the file.

Depending on the desired dimensionaltiy of the final plot, the scripts differ
here.

### 1D
##### Generator Script

To generate 1D plots using a so-called 'NICS probe', these scripts should be
used. To generate the ghost atoms, `1d_gen.py` will be used.

To use this script, type:

```sh
1d_gen.py
```

followed by 2 required positional arguments, and 1 of 3 mutually exclusive
arguments. The 1st should be the name of the new input file, and the 2nd should
be the name of the new file to be written to, ***without the file extension***.
Note that if more than 100 ghost atoms will be generated, more than 1 file will
be generated. The mutually exclusive arguments are either `-x`, `-y`, or `-z`,
which must be specified to denote the direction for which the ghost atom array
will be added to.

For example, if the input file `start_benzene.com` were to be used, the
simplest syntax would be as follows:

```sh
1d_gen.py start_benzene.com benzene_1d -x
```

which would append ghost atoms to the file in the x-direction of the file
`benzene_1d.com`. Following this, the following prompt will print:

```
Enter start coordinates (x, y, z) for the first ghost atom separated by spaces:
```

Unless the `-d, --define_spacings` argument is specified.

Input the 3D coordinate of the first ghost atom. For the next prompt type the
last ghost atom coordinate, and finally the distance (or vector space) between
each atom for the final prompt. This might look like:
```
Enter start coordinates (x, y, z) for the first ghost atom separated by spaces: -5 0 1
Enter end coordinates (x, y, z) for the last ghost atom separated by spaces: 5 0 1
Specify the 1D vector spacings: 0.2
```

Where each coordinate is equal to 1 &#8491; long. It is recommended to use
vector spacings of 0.2 &#8491;.

The file(s) will now be automatically generated with a maximum of 100 ghost
atoms per file, unless<br /> `-n [NUMBER], --number [NUMBER]` is specified. 

The following is the result of invoking `1d_gen.py -h`, which describes all of
the optional arguments.

```
  -h, --help                      show this help message and exit
  -c, --chkfile                   include a line in the input file(s) which
                                  will generate a Gassian .chk file in addition
                                  to a .log file (MUST ALREADY have a line
                                  specifying nprocs as per the Guassian manual)
  -d, --define_spacings           generate ghost atoms by defining vector
                                  spacings rather than start and end coordinates
  -n [NUMBER], --number [NUMBER]  specify the number of ghost atoms to write
                                  per file (default = 100). It might be useful
                                  to reduce this value if any of jobs fail when
                                  running on Gaussian
  -v, --verbose                   print output of Bq coordinates to append to file
```

To learn how to run jobs and parse these output files, see 
[Running Multiple Jobs](#running-multiple-jobs), and [Parsing Output
Files](#parsing-output-files).

##### Graphing Script

### 2D

### 3D

Currently, the 3D scripts are still in active development. When completed, they
will be documented here.

### Running Multiple Jobs

To automate running multiple Gaussian jobs serially, the bash script `mg09.sh`
can be used, followed by the files to be run. This script works with all bash
wildcards so each file doesn't have to be input individually. For example, if
it is executed in a directory containing many input files which start with xy,
the script and files can be called with:
```sh
mg09.sh xy*.com
```

If you are accessing Gaussian through an `ssh` session, copy to the script to the
machine hosting the `ssh` to `$HOME` (possible using `sshfs`), and add the 
location of the script to the shell `$PATH`.

### Parsing Output Files

`log_parser.py` is used to parse the information from the Gaussian output
files, which takes the input file and the output file as positional arguments.
If benzene_1d.com and benzene_1d.log are these files:

```sh
log_parser.py benzene_1d.com benzene_1d.log 
```

`log_parser.py` has the following command line options:

```
-h, --help                            show this help message and exit
-f [FILENAME], --filename [FILENAME]  specify custom name to save parsed log data file as
-v, --verbose                         print output of file containing parsed data
```

However, it is likely you will be working with multiple input and output files.
For this, `mparse.sh` was written. Similarly to `mg09.sh`, files don't need to
be individually specified. As long as all input and output files have a
similarity in their names, this can be used to specify all files to be parsed
in a directory. 

For instance, if the following files are in a directory:
```sh
xy_benzene_1.com    xy_benzene_2.com
xy_benzene_1.log    xy_benzene_2.log
```
```sh
mparse.py xy* 
```
can be used to call all these files to be parsed, which will result in the
following output:
```sh
2 input and 2 output files selected.

Input files: xy_benzene_1.com xy_benzene_2.com

Output files: xy_benzene_1.log xy_benzene_2.log
```

Note that there must be the same number of input and output files selected for
this to work.

## Contributors

Dylan Morgan

Supervisor: Dr Felix Plasser

Research Group: https://fplasser.sci-public.lboro.ac.uk/

Institution: Loughborough University

Copyright © 2020-2021, Dylan Morgan and Felix Plasser
