#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
import scipy.odr as sodr
from tools import getRootDirectory, getOutputFilename, getColorIterator
import csv
import numpy as np

import argparse
import pathlib
import configparser

# parse CLI arguments
parser = argparse.ArgumentParser(description='Plot the energy depending on the value of hbar sample.')
parser.add_argument('filename', type=pathlib.Path, help='Input filename')
parser.add_argument('-o', '--output', type=pathlib.Path, help='Output filename')
args = parser.parse_args()

# filesystem stuff
root_path = getRootDirectory()


full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print('\033[1m[Classical limit energy]\033[0m Computing file %s ... ' %relative_path, end='')

hbars = []
energies = []
denergies = []

# read csv file
with full_path.open('r') as csvfile:
	reader = csv.reader(csvfile)
	for i, row in enumerate(reader):
		if i < 2:
			continue
		hbars.append(float(row[0]))
		energies.append(float(row[1]))
		denergies.append(float(row[2]))

hbars = np.array(hbars)


# plot
plt.figure()

color_iterator = getColorIterator()
color_plot, color_fit = next(color_iterator)['color']

plt.errorbar(hbars, energies, yerr=denergies, fmt='.', label='data', color=color_plot)
plt.xlabel(r'$\hbar$')
plt.ylabel('energy')

def linear(p, x):
	a, b = p
	return a * x + b


initvals = [1, 0]

model = sodr.Model(linear)

fit_data = sodr.RealData(hbars, energies, sy=denergies)

odr = sodr.ODR(fit_data, model, beta0=initvals)
out = odr.run()

parameters = out.beta
parameters_error = out.sd_beta


xdata_fit = np.linspace(min(hbars), max(hbars), 1000)
ydata_fit = linear(parameters, xdata_fit)
plt.plot(xdata_fit, ydata_fit, label=r'fit: $E=(%.1f \pm %.1f) \cdot \hbar + (%.1f \pm %.1f)$' %(parameters[0], parameters_error[0], parameters[1], parameters_error[1]), color=color_fit)
plt.legend()


# filesystem stuff
out_filename = getOutputFilename(relative_path, '', args.output)

out_filename_slope = pathlib.Path('%s_slope.tex' %out_filename.with_suffix(''))
with open(out_filename_slope, 'w') as f:
	f.write(r'$\frac\omega2=\SI{%0.1f +- %0.1f}{}$' %(parameters[0], parameters_error[0]))

out_filename_offset = pathlib.Path('%s_offset.tex' %out_filename.with_suffix(''))
with open(out_filename_offset, 'w') as f:
	f.write(r'$E_0=\SI{%0.1f +- %0.1f}{}$' %(parameters[1], parameters_error[1]))

# write to disk
plt.savefig(out_filename)
print('done')