#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, getColorIterator, autoCorrelationNormalized, getIntegratedCorrelationTime
import csv
import numpy as np

import argparse
import pathlib
import configparser

color_iterator = getColorIterator()

# parse CLI arguments
parser = argparse.ArgumentParser(description='Calculate the autorelation function.')
parser.add_argument('filename', type=pathlib.Path, help="Input filename")
parser.add_argument('-i', '--iterations', nargs='+')
parser.add_argument('-o', '--output', type=pathlib.Path, help="Output filename")
args = parser.parse_args()

# filesystem stuff
root_path = getRootDirectory()

iterations_used = [int(i) for i in args.iterations]

full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)


relative_path = full_path.relative_to(root_path / 'data')

print('[Autocorrelation] Computing file %s ... ' %relative_path, end='')

data = {}

config = configparser.ConfigParser()
config.read(full_path.with_suffix('.cfg'))

# read config from respective file
tau = config['DEFAULT'].getfloat('tau', fallback=0.1)

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

for iteration in iterations_used:
	# get fitting color pair
	color_plot, color_fit = next(color_iterator)['color']
	ydata_sum = np.zeros(len(numbers))
	for i in range(iteration, iteration + 10):
		xdata = numbers
		positions = data[iteration]
		# calculate autocorrelation
		ydata = autoCorrelationNormalized(positions * positions, xdata)
		xdata_times = xdata * 0.1

		ydata_sum += ydata

	# calculate integrated autocorrelation time
	tint = getIntegratedCorrelationTime(ydata_sum, factor=8) * tau

	ydata_mean = ydata_sum / len(ydata_sum)
	plt.errorbar(xdata_times, ydata_mean, label=r'autocorrelation after %d iteration%s, $\tau_{int} = %0.4f$' %(iteration, 's' if iteration > 1 else '', tint), fmt='.', color=color_plot)
	# plot and fit

plt.xlabel('Time t')
plt.ylabel('$\Gamma(t)$')
plt.yscale('log')
plt.xlim(-0.1, 1)
plt.legend()


out_filename = root_path / 'imgs' / relative_path
out_filename.parent.mkdir(parents=True, exist_ok=True)

out_filename = out_filename.with_suffix('')
out_filename = pathlib.Path('%s_autocorrelation_%s' %(out_filename, '-'.join([str(i) for i in iterations_used])))

if args.output:
	out_filename = args.output
out_filename.parent.mkdir(parents=True, exist_ok=True)

# write to disk
plt.savefig(out_filename)
print('done')