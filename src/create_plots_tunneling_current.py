#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, getOutputFilename
import csv
import numpy as np

import argparse
import pathlib
import configparser

# parse CLI arguments
parser = argparse.ArgumentParser(description='Plot the energy depending on the metropolis sample.')
parser.add_argument('filename', type=pathlib.Path, help='Input filename')
parser.add_argument('-o', '--output', type=pathlib.Path, help='Output filename')
args = parser.parse_args()

# filesystem stuff
root_path = getRootDirectory()


full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print('\033[1m[Tunnelling current]\033[0m Computing file %s ... ' %relative_path, end='')

distances = []
transitions = []
dtransitions = []

# read csv file
with full_path.open('r') as csvfile:
	reader = csv.reader(csvfile)
	for i, row in enumerate(reader):
		if i < 2:
			continue
		distances.append(float(row[0]))
		transitions.append(float(row[-2]))
		dtransitions.append(float(row[-1]))

distances = np.array(distances)
transitions = np.array(transitions)
dtransitions = np.array(dtransitions)

# read config from respective file
config = configparser.ConfigParser()
config.read(full_path.with_suffix('.cfg'))

N = config['DEFAULT'].getfloat('n', fallback=100)

# plot
plt.figure()

plt.errorbar(distances, transitions / N, yerr = dtransitions / N, fmt='.')
plt.xlabel('Distance')
plt.ylabel('Tunneling rate')


# filesystem stuff
out_filename = getOutputFilename(relative_path, 'tunneling_current', args.output)

# write to disk
plt.savefig(out_filename)
print('done')