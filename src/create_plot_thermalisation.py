#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, Energy, Kinetic, Potential, autoCorrelationNormalized, autoCorrelationNormalizedError, getIntegratedCorrelationTime, getOutputFilename, running_mean, block
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

print('\033[1m[Thermalisation]\033[0m Computing file %s ... ' %relative_path, end='')

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


xdata = np.array(list(data.keys()))

# generate objects to measure the energy
k = Kinetic(m, tau)

p = Potential(mu, lambda_)

e = Energy(k, p)
ydata = np.array([e(data[x]) for x in xdata])

# calculate mean energy
d = ydata[:-1] - ydata[1:]
da = running_mean(d, 10)
if da[0] > 0:
	start = np.argmax(da < 0) + 10
else:
	start = np.argmax(da > 0) + 10


# filesystem stuff
out_filename = getOutputFilename(relative_path, 'thermalisation', args.output)
out_filename_autocorrelation = pathlib.Path('%s_autocorrelation.pdf' %out_filename.with_suffix(''))


ydata_cut = autoCorrelationNormalized(ydata, np.arange(len(ydata)))

# calculate integrated autocorrelation time
tint, dtint, w_max = getIntegratedCorrelationTime(ydata_cut, factor=8)

step_size = int((tint + dtint) * 2 + 1)

xdata_cut = xdata[start::step_size]

# calculate mean over blocked data
ydata_mean = block(ydata[start:], step_size)

ydata_ac_cut = autoCorrelationNormalized(ydata_mean, np.arange(len(xdata_cut)))
ydata_ac_cut_err = autoCorrelationNormalizedError(ydata_ac_cut, len(ydata_mean), 10)

# calculate energy
energy, denergy = np.mean(ydata_mean), np.std(ydata_mean)

# create autocorrelation plot
plt.figure()
plt.errorbar(xdata_cut[:2 * w_max // step_size], ydata_ac_cut[:2 * w_max // step_size], yerr=ydata_ac_cut_err[:2 * w_max // step_size], label=r'$\tau_{int} = %0.4f \pm %0.4f$' %(tint, dtint), fmt='.')
plt.xlabel('Sample')
plt.ylabel('Autocorrelation')
plt.legend()
plt.savefig(out_filename_autocorrelation)

# plot
plt.figure()
plt.errorbar(block(xdata[:max_iteration], step_size), block(ydata[:max_iteration], step_size), yerr=block(ydata[:max_iteration], step_size, func=np.std), label=r'energy $\bar{E} = (%.2f \pm %.2f) \cdot 10^3$' %(energy / 1000, denergy / 1000), fmt='.')
plt.xlabel('Number')
plt.ylabel('Energy')
if args.log:
	plt.yscale('log')
plt.legend()

# write to disk
plt.savefig(out_filename)
print('done')