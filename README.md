# Harmonic Oscillator

This Repository holds everything that was programmed for the project 'Harmonic Oscillator', part of the module physics760: Computational Physics.

## Prerequisites
The scripts depend on various libraries, presented below. These have to be installed for the used Python Version. Python 3 was used for development, which is the recommended version to run these scripts.
| Library      |     Description                                                        | Tested Version |
|--------------|------------------------------------------------------------------------|----------------|
| numpy        |  Library containing a lot of function regarding numerical calculations | 1.16.2         |
| scipy        |    Library scientific library, contains for example fit algorithms     | 1.1.0          |
| pathlib      | Library containing convenient classes to handle files and directories  | 1.0.1          |
| configparser | Used to handle command line parameters                                 | 3.0.2          |
| statsmodels  | Library that contains function for statistical analysis, i.e. qq plots | 0.11.1         |
| cycler       | Library used to deal with the color scheme                             | 0.10.0         |
| matplotlib   | Library that creates most of the plots                                 | 3.0.2-2        |

## Installation
The above mentioned libraries can be installed using the following command:
```bash
pip3 install numpy scipy pathlib configparser statsmodels cycler
apt install python3-matplotlib
```
`matplotlib` should be installed via a package manager, since the pypy version has some bugs leading to error massages.

The libraries basically have corresponding functions in `R`. Every function that is not present in `R` has been programmed manually in `tools.py`.