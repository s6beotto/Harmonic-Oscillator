#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, getColorIterator, autoCorrelationNormalized, getIntegratedCorrelationTime
import csv
import numpy as np
import scipy.optimize as op

import argparse
import pathlib

color_iterator = getColorIterator()

def linear(x, *p):
	a, b = p
	return a * x + b

# parse CLI arguments
parser = argparse.ArgumentParser(description='Calculate the autorelation function between the metropolis samples.')
parser.add_argument('filename', type=pathlib.Path, help="Input filename")
parser.add_argument('-f', '--fit', action='store_true')
parser.add_argument('-o', '--output', type=pathlib.Path, help="Output filename")
args = parser.parse_args()

# filesystem stuff
root_path = getRootDirectory()

full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print('[Autocorrelation Metropolis] Computing file %s ... ' %relative_path, end='')

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

plt.figure()

metropolis_iterations = np.array(sorted(data.keys()))

data = np.array([data[num] for num in metropolis_iterations])

# get fitting color pair
color_plot, color_fit = next(color_iterator)['color']
ydata_sum = np.zeros(len(metropolis_iterations))
xdata = metropolis_iterations

# calculate autocorrelation
for i in range(data.shape[1]):
	positions = data[:,i]
	ydata = autoCorrelationNormalized(positions, xdata)

	ydata_sum += ydata

# calculate integrated autocorrelation time
tint = getIntegratedCorrelationTime(ydata_sum, factor=8)

# plot and fit
ydata_mean = ydata_sum / data.shape[1]
plt.errorbar(xdata, ydata_mean, label='Autocorrelation function, $\tau_{int} = $' %(tint), fmt='.', color=color_plot)
if args.fit:
	xdata, ydata_mean = xdata[xdata < 50], ydata_mean[xdata < 50]
	xdata, ydata_mean = xdata[ydata_mean > 0], ydata_mean[ydata_mean > 0]
	parameters, parameters_error = op.curve_fit(linear, xdata, np.log(ydata_mean), p0=[1, 1])
	parameters_error = np.sqrt(np.diag(parameters_error))
	xdata_fit = np.linspace(min(xdata), max(xdata), 1000)
	ydata_fit = linear(xdata_fit, *parameters)
	plt.plot(xdata_fit, np.exp(ydata_fit), color=color_fit)

plt.xlabel('Metropolis iteration')
plt.ylabel('$\Gamma(t)$')
plt.yscale('log')
plt.legend()

plt.xlim(min(xdata), max(xdata))

out_filename = root_path / 'imgs' / relative_path
out_filename.parent.mkdir(parents=True, exist_ok=True)

out_filename = out_filename.with_suffix('')
out_filename = pathlib.Path('%s_autocorrelation_metropolis' %(out_filename))

if args.output:
	out_filename = args.output
out_filename.parent.mkdir(parents=True, exist_ok=True)

# write to diskydata_sum
plt.savefig(out_filename)
print('done')