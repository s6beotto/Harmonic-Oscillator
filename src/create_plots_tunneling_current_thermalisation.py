#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, Energy, Kinetic, Potential, autoCorrelationNormalized, countTransitions, getOutputFilename, running_mean
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

print('[Track tunneling current] Computing file %s ... ' %relative_path, end='')

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

# read config from respective file
config = configparser.ConfigParser()
config.read(full_path.with_suffix('.cfg'))

N = config['DEFAULT'].getfloat('n', fallback=100)


xdata = list(data.keys())

ydata = np.array([countTransitions(data[x]) for x in xdata]) / N

# calculate mean energy
d = ydata[:-1] - ydata[1:]
da = running_mean(d, 30)
print(da)
if da[0] > 0:
	start = np.argmax(da < 0) + 10
else:
	start = np.argmax(da > 0) + 10

print(start)

to_use = ydata[start::30]


# filesystem stuff
out_filename = getOutputFilename(relative_path, 'tunneling_current_thermalisation', args.output)
out_filename_autocorrelation = pathlib.Path('%s_autocorrelation.pdf' %out_filename.with_suffix(''))

# calculate tunneling current
tunneling_current, dtunneling_current = np.mean(to_use), np.std(to_use)
print(tunneling_current, dtunneling_current)

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
plt.errorbar(xdata[:max_iteration], ydata[:max_iteration], label=r'tunneling rate = $%.2f \pm %.2f$' %(tunneling_current, dtunneling_current))
plt.xlabel('Number')
plt.ylabel('tunneling current')
if args.log:
	plt.yscale('log')
plt.legend()

out_filename.parent.mkdir(parents=True, exist_ok=True)

# write to disk
plt.savefig(out_filename)
print('done')