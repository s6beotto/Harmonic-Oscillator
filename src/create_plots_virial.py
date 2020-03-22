#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, Energy, Kinetic, Potential, autoCorrelationNormalized, getTotalKineticEnergy, getTotalPotentialEnergy, getOutputFilename, block
import csv
import numpy as np

import argparse
import pathlib
import configparser

# parse CLI arguments
parser = argparse.ArgumentParser(description='Plot the energy depending on the metropolis sample.')
parser.add_argument('filename', type=pathlib.Path, help='Input filename')
parser.add_argument('-i', '--max_iteration', type=int)
parser.add_argument('-l', '--log', action='store_true')
parser.add_argument('-o', '--output', type=pathlib.Path, help='Output filename')
args = parser.parse_args()

# filesystem stuff
root_path = getRootDirectory()

max_iteration = args.max_iteration

full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print('\033[1m[Virial]\033[0m Computing file %s ... ' %relative_path, end='')

data = {}

# read csv file
with full_path.open('r') as csvfile:
	reader = csv.reader(csvfile)
	for i, row in enumerate(reader):
		if i == 0:
			numbers = np.array([int(r) for r in row[1:]])
			pass
		else:
			num = int(row[0])
			positions = np.array([float(r) for r in row[1:]])
			data[num] = positions

config = configparser.ConfigParser()
config.read(full_path.with_suffix('.cfg'))

# read config from respective file
m = config['DEFAULT'].getfloat('mass', fallback=1.0)
tau = config['DEFAULT'].getfloat('tau', fallback=1.0)
mu = config['DEFAULT'].getfloat('mu', fallback=1.0)
lambda_ = config['DEFAULT'].getfloat('lambda_', fallback=0)

xdata = list(data.keys())

# generate objects to measure the energy
k = Kinetic(m, tau)

p = Potential(mu, lambda_)

block_size = 10

xdata_cut = xdata[::block_size]

kineticE = block(np.array([getTotalKineticEnergy(data[x], k) for x in xdata]), block_size)
potentialE = block(np.array([getTotalPotentialEnergy(data[x], p) for x in xdata]), block_size)

# filesystem stuff
out_filename = getOutputFilename(relative_path, 'virial', args.output)

start = 100 // block_size
potentialE_mean = np.mean(potentialE[start:])
potentialE_error = np.std(potentialE[start:])
kineticE_mean = np.mean(kineticE[start:])
kineticE_error = np.std(kineticE[start:])

# plot
plt.figure()
plt.fill_between(xdata_cut, potentialE + kineticE, kineticE, alpha=0.75, label=r'potential energy $\bar E = (%0.1f \pm %0.1f)$' %(potentialE_mean, potentialE_error))
plt.fill_between(xdata_cut, kineticE, alpha=0.75, label=r'kinetic energy $\bar E = (%0.1f \pm %0.1f)$' %(kineticE_mean, kineticE_error))

plt.xlabel('Number')
plt.ylabel('Energy')
if args.log:
	plt.yscale('log')
plt.legend()

# write to disk
plt.savefig(out_filename)
print('done')