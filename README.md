# Harmonic Oscillator

This Repository holds everything that was programmed for the project 'Harmonic Oscillator', part of the module physics760: Computational Physics.

## Prerequisites
The scripts depend on various libraries, presented below. These have to be installed for the used Python Version. Python 3 (3.7.3 Dec 20 2019) was used for development, which is the recommended version to run these scripts.
| Library      |     Description                                                        | Tested Version |
|--------------|------------------------------------------------------------------------|----------------|
| numpy        |  Library containing a lot of function regarding numerical calculations | 1.16.2         |
| scipy        |    Library scientific library, contains for example fit algorithms     | 1.1.0          |
| pathlib      | Library containing convenient classes to handle files and directories  | 1.0.1          |
| configparser | Used to handle command line parameters                                 | 3.0.2          |
| statsmodels  | Library that contains function for statistical analysis, i.e. qq plots | 0.11.1         |
| cycler       | Library used to deal with the color scheme                             | 0.10.0         |
| matplotlib   | Library that creates most of the plots                                 | 3.0.2-2        |

## Dependencies
The above mentioned libraries can be installed using the following command. Additionally `make`, `g++` and obviously `python3` are needed.
```bash
apt install make g++ python3 python3-matplotlib python3-pip
pip3 install numpy scipy pathlib configparser statsmodels cycler
```
`matplotlib` should be installed via a package manager, since the pypy version has some bugs leading to error massages.

The libraries basically have corresponding functions in `R`. Every function that is present in `R`, but not in `Python` has been programmed manually in `tools.py`.

If the software should assemble the final pdf files, the required packages can be installed using
```bash
sudo apt install texlive texlive-science texlive-latex-recommended texlive-latex-extra texlive-fonts-extra
```

## Usage
When all the dependencies are installed one can start the software.
First of all, the `C` library has to be compiled.
For this one can use the makefile as following
```bash
make compile
```
The `C` version of the central algorithm is roughly 8 times faster than the `Python` version.
To explicitly use the `Python` version, the comment in the last line of `tools.py` has to be removed, a compile is thus not necessary.
This makes sure that the software runs on every system where `Python3` is present.

To run the software simply use
```bash
make plots
```
This generates firstly all data file in the `data` directory, then generates plots in the `imgs` directory.

If the report and the slides should be generated, the command
```bash
make
```
is used, which first generates all requisite files, if they are not present and then assembles the pdf files.
For this the latex-related packages above have to be present.

Since many of the required steps are independent, one can use the multi processing feature of make as.
But because many of the executed scripts already use multiprocessing, this only has a very small influence, but greatly increases RAM usage.
```bash
make -j
```
This causes make to run with many processes in parallel, depending on the number of logical CPU cores. On my quad-core processor (Intel i7-4770) this process took around 5 minutes and used a peak of around 1GB of RAM and 100% CPU load.

To clean up the directory simply type
```bash
make clean
```

## Acknowledgement
Note:
Commits done by my former project partner have been undone, I only use content that I created myself and code that I reference.

I use the latexrun.py file provided by Austin Clements, from https://github.com/aclements/latexrun.