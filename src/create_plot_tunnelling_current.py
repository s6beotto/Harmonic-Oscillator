#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
import scipy.optimize as op
from tools import getRootDirectory, getOutputFilename, getColorIterator
import csv
import numpy as np

import argparse
import pathlib
import configparser

# parse CLI arguments
parser = argparse.ArgumentParser(description='Plot the energy depending on the metropolis sample.')
parser.add_argument('filename', type=pathlib.Path, help='Input filename')
parser.add_argument('-l', '--log', action='store_true')
parser.add_argument('-f', '--fit', type=float, default=None, help='Fit an exponential function to the data, starting with the given value')
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

color_iterator = getColorIterator()
color_plot, color_fit = next(color_iterator)['color']

plt.errorbar(distances, transitions / N, yerr = dtransitions / N, fmt='.', color=color_plot)
plt.xlabel('Distance')
plt.ylabel('tunnelling rate')
if args.log:
	plt.yscale('log')

# filesystem stuff
out_filename = getOutputFilename(relative_path, 'tunnelling_current', args.output)

if args.fit:
	def exp_decay(x, *p):
		A, c = p
		return A * np.exp(-x / c)

	initvals = [1, 1]
	filter_ = (distances > args.fit) * (transitions > 5)
	parameters, parameters_error = op.curve_fit(exp_decay, distances[filter_], transitions[filter_] / N, p0=initvals, sigma=dtransitions[filter_] / N)

	parameters_error = np.sqrt(np.diag(parameters_error))

	xdata_fit = np.linspace(min(distances), max(distances), 1000)
	ydata_fit = exp_decay(xdata_fit, *parameters)

	plt.plot(xdata_fit, ydata_fit, scaley=False, label='$f(x) = A \cdot \exp(-x / b)$\n$A = (%.0f \pm %.0f)$\n$b = (%.2f \pm %.2f)$' %(parameters[0], parameters_error[0], parameters[1], parameters_error[1]), color=color_fit)
	plt.legend()

	# save slope of the fit
	out_filename_slope = pathlib.Path('%s_slope.tex' %out_filename.with_suffix(''))
	with open(out_filename_slope, 'w') as f:
		f.write(r'$b=\SI{%0.2f +- %0.2f}{}$' %(parameters[1], parameters_error[1]))

# write to disk
plt.savefig(out_filename)
print('done')