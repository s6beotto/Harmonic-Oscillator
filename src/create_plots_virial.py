#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, Energy, Kinetic, Potential, autoCorrelationNormalized, getTotalKineticEnergy, getTotalPotentialEnergy, getOutputFilename
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

print('[Track] Computing file %s ... ' %relative_path, end='')

data = {}
print(1)

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

kineticE = np.array([getTotalKineticEnergy(data[x], k) for x in xdata[::10]])
potentialE = np.array([getTotalPotentialEnergy(data[x], p) for x in xdata[::10]])

for i in range(0, len(xdata) // 10):
	print(kineticE[i], potentialE[i])


exit(-1)


# filesystem stuff
out_filename = getOutputFilename(relative_path, 'virial', args.output)
#out_filename_autocorrelation = pathlib.Path('%s_autocorrelation.pdf' %out_filename.with_suffix(''))

# calculate energy
energy, denergy = np.mean(to_use), np.std(to_use)

xdata_cut = xdata[start::30]
ydata_cut = autoCorrelationNormalized(ydata[start::30], np.arange(len(xdata_cut)))

# create autocorrelation plot
plt.figure()
plt.errorbar(xdata_cut, ydata_cut)
plt.xlabel('Sample')
plt.ylabel('Autocorrelation')
plt.savefig(out_filename_autocorrelation)

# plot
plt.figure()
plt.errorbar(xdata[:max_iteration], ydata[:max_iteration], label=r'energy $\bar{E} = (%.2f \pm %.2f) \cdot 10^3$' %(energy / 1000, denergy / 1000))
plt.xlabel('Number')
plt.ylabel('Energy')
if args.log:
	plt.yscale('log')
plt.legend()

# write to disk
plt.savefig(out_filename)
print('done')