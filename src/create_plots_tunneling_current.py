#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, Energy, Kinetic, Potential, bootstrap
import csv
import numpy as np

import argparse
import pathlib
import configparser

# parse CLI arguments
parser = argparse.ArgumentParser(description='Plot the energy depending on the metropolis sample.')
parser.add_argument('filename', type=pathlib.Path, help="Input filename")
parser.add_argument('-o', '--output', type=pathlib.Path, help="Output filename")
args = parser.parse_args()

# filesystem stuff
root_path = getRootDirectory()


full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print("[Tunneling current] Computing file %s ... " %relative_path, end='')

distances = []
transitions = []

# read csv file
with full_path.open('r') as csvfile:
	reader = csv.reader(csvfile)
	for i, row in enumerate(reader):
		if i < 2:
			continue
		distances.append(float(row[0]))
		transitions.append(int(row[-1]))

distances = np.array(distances)
transitions = np.array(transitions)

plt.figure()

config = configparser.ConfigParser()
config.read(full_path.with_suffix('.cfg'))


# plot
config = configparser.ConfigParser()
config.read(full_path.with_suffix('.cfg'))


# read config from respective file
N = config['DEFAULT'].getfloat('n', fallback=100)

plt.errorbar(distances, transitions / N, fmt='.')
plt.xlabel('Distance')
plt.ylabel('Tunneling rate')


out_filename = root_path / 'imgs' / relative_path

out_filename = out_filename.with_suffix('')
out_filename = pathlib.Path('%s_tunneling_current.pdf' %(out_filename))
if args.output:
	out_filename = args.output
out_filename.parent.mkdir(parents=True, exist_ok=True)

# write to disk
plt.savefig(out_filename)
print('done')