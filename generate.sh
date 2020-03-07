#!/bin/bash

PYTHON="/usr/bin/python3"

if [ "${1}" = "-h" ] || [ "${1}" = "--help" ]; then
    echo "usage: ${0} [-h] [-c] [-f]"
	echo
	echo "Create and plot the data"
	echo
	echo "optional arguments:"
	echo "  -h, --help		show this help message and exit"
	echo "  -c, --clean		clean data and image directories"
	echo "  -f, --force		force overwrite of data files"
    exit 1
fi

# cleanup
if [ "${1}" = "-c" ] || [ "${1}" = "--clean" ]; then
    rm -r data/* 2> /dev/null
    rm -r imgs/* 2> /dev/null
    exit 1
fi

# harmonic oscillator
if [ "${1}" = "-f" ] || [ "${1}" = "--force" ]; then
    force=true
else
    force=false
fi

# evolution of path from 5 to 0
FILE=data/harmonic_oscillator_track/N100i100init5.0000m0.2500.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/harmonic_oscillator.py -m 0.25 -init 5 -ir 1 -i 100 -N 100 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_track.py $FILE -i 1 10 20 40 80 100
$PYTHON src/create_plots_gauss.py $FILE -i 1 10 20 40 80 100 -f
$PYTHON src/create_plots_gauss.py $FILE -i 10 20 40 80 100 -f

echo

# evolution of path from 5 to 0
FILE=data/harmonic_oscillator_track/N1000i100init5.0000m0.2500.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/harmonic_oscillator.py -m 0.25 -init 5 -ir 1 -i 100 -N 1000 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_track.py $FILE -i 1 10 20 40 80 100
$PYTHON src/create_plots_gauss.py $FILE -i 1 10 20 40 80 100 -f
$PYTHON src/create_plots_gauss.py $FILE -i 10 20 40 80 100 -f

echo

# evolution of path from 5 to 0
FILE=data/harmonic_oscillator_track/N10000i100init5.0000m0.2500.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/harmonic_oscillator.py -m 0.25 -init 5 -ir 1 -i 100 -N 10000 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_track.py $FILE -i 1 10 20 40 80 100
$PYTHON src/create_plots_gauss.py $FILE -i 1 10 20 40 80 100 -f
$PYTHON src/create_plots_gauss.py $FILE -i 10 20 40 80 100 -f
$PYTHON src/create_plots_gauss.py $FILE -i 1 -f
$PYTHON src/create_plots_gauss.py $FILE -i 10 -f
$PYTHON src/create_plots_gauss.py $FILE -i 20 -f
$PYTHON src/create_plots_gauss.py $FILE -i 40 -f
$PYTHON src/create_plots_gauss.py $FILE -i 80 -f
$PYTHON src/create_plots_gauss.py $FILE -i 100 -f
$PYTHON src/create_plots_qq.py $FILE -i 1
$PYTHON src/create_plots_qq.py $FILE -i 10
$PYTHON src/create_plots_qq.py $FILE -i 20
$PYTHON src/create_plots_qq.py $FILE -i 40
$PYTHON src/create_plots_qq.py $FILE -i 80
$PYTHON src/create_plots_qq.py $FILE -i 100

echo

# evolution of path from 5 to 0 better
FILE=data/harmonic_oscillator_track/N1000i1000init5.0000m0.2500.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/harmonic_oscillator.py -m 0.25 -init 5 -ir 1 -i 1000 -N 1000 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_track.py $FILE -i 1 10 20 40 80 100 1000
$PYTHON src/create_plots_gauss.py $FILE -i 1 10 20 40 80 100 1000 -f
$PYTHON src/create_plots_gauss.py $FILE -i 10 20 40 80 100 1000 -f

echo

# evolution of a step state
FILE=data/harmonic_oscillator_track/N100i100initstepm0.2500step.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/harmonic_oscillator.py -m 0.25 -i 100 -N 100 --step -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_track.py $FILE -i 1 10 20 40 80 100
$PYTHON src/create_plots_track_shifted.py $FILE -i 1 10 20 40 80 100
$PYTHON src/create_plots_track_shifted.py $FILE -i 1 5 10 15 20 25
$PYTHON src/create_plots_track_shifted.py $FILE -i 1 2 3 4 5 6 7 8 9 10
$PYTHON src/create_plots_track_shifted.py $FILE -i 1 3 5 7 9 11 13 15
$PYTHON src/create_plots_qq.py $FILE -i 1
$PYTHON src/create_plots_qq.py $FILE -i 10
$PYTHON src/create_plots_qq.py $FILE -i 20
$PYTHON src/create_plots_qq.py $FILE -i 40
$PYTHON src/create_plots_qq.py $FILE -i 80
$PYTHON src/create_plots_qq.py $FILE -i 100

echo


# anharmonic oscillator
FILE=data/anharmonic_oscillator_track/N100i1000init0.0m0.2500l-0.0200d10.0000.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/anharmonic_oscillator.py -m 0.25 -init 0 -ir 10 -i 1000 -N 100 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_track.py $FILE -i 1 10 20 40 80 100 1000
$PYTHON src/create_plots_track.py $FILE -i 1 50 100 200 400 1000

echo

FILE=data/anharmonic_oscillator_track/N1000i1000init0.0m0.2500l-0.0200d10.0000.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/anharmonic_oscillator.py -m 0.25 -init 0 -ir 10 -i 1000 -N 1000 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_track.py $FILE -i 1 10 20 40 80 100 1000

echo

FILE=data/anharmonic_oscillator_track/N100i10000init0.0m0.2500l-0.0200d10.0000.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/anharmonic_oscillator.py -m 0.25 -init 0 -ir 10 -i 10000 -N 100 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_track.py $FILE -i 100 1000 2000 3000 5000 10000

echo

FILE=data/anharmonic_oscillator_track/N200i10000init0.0m0.2500l-0.0200d10.0000.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/anharmonic_oscillator.py -m 0.25 -init 0 -ir 10 -i 10000 -N 200 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_track.py $FILE -i 100 1000 2000 3000 5000 10000

echo

# classical limit harmonic oscillator
FILE=data/harmonic_oscillator_classical_limit/h0.00-2.00-0.0100_-5.00-5.00-0.10-N1000.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/harmonic_oscillator_classical_limit.py -N 1000 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_classical_limit.py $FILE

echo

FILE=data/harmonic_oscillator_classical_limit/h0.00-2.00-0.0100_-3.00-3.00-0.05-N1000.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/harmonic_oscillator_classical_limit.py -N 1000 -b " -3:3:0.05" -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_classical_limit.py $FILE

echo

# classical limit anharmonic oscillator
FILE=data/anharmonic_oscillator_classical_limit/h0.00-2.00-0.0100_-5.00-5.00-0.05-N1000d4.0000.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/anharmonic_oscillator_classical_limit.py -N 1000 -b " -5:5:0.05" -init -5 -ir 2 -i 1000 -d 4 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_classical_limit.py $FILE

echo

# lambda parameter anharmonic oscillator
FILE=data/anharmonic_oscillator_lambda_parameter/d0.00-10.00-0.10s-5.00-5.00-0.10-N1000-i100.csv
if [ ! -f $FILE ] || [ "$force" = true ]; then
    echo "Generating file $FILE"
    $PYTHON src/anharmonic_oscillator_lambda_parameter.py -init 0 -ir 10 -i 100 -N 1000 -o $FILE
else
    echo "Not generating file $FILE"
fi
$PYTHON src/create_plots_lambda_parameter.py $FILE

echo