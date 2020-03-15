# Harmonic Oscillator

This Repository holds everything that was programmed for the project 'Harmonic Oscillator', part of the module physics760: Computational Physics.

## Prerequisites
The scripts depend on various libraries, presented below. These have to be installed for the used Python Version. Python 3 was used for development, which is the recommended version to run these scripts.
| Library      |     Description                                                        |
|--------------|------------------------------------------------------------------------|
| numpy        |  Library containing a lot of function regarding numerical calculations |
| scipy        |    Library scientific library, contains for example fit algorithms     |
| pathlib      | Library containing convenient classes to handle files and directories  |
| configparser | Used to handle command line parameters                                 |
| statsmodels  | Library that contains function for statistical analysis, i.e. qq plots |
| cycler       | Library used to deal with the color scheme                             |
| matplotlib   | Library that creates most of the plots                                 |

## Installation
The above mentioned libraries can be installed using the following command:
```bash
pip3 install numpy scipy pathlib configparser statsmodels
```

The libraries basically have corresponding functions in `R`. Every function that is not present in `R` has been programmed manually in `tools.py`.