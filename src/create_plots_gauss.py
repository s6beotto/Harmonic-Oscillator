from matplotlib import pyplot as plt
import matplotlib
from tools import getRootDirectory, getColorIterator
import csv
import numpy as np
import scipy.optimize as op

import argparse
from glob import glob

import itertools
flatten = itertools.chain.from_iterable

color_iterator = getColorIterator()

def gauss(x, *p):
	A, mu, sigma = p
	return A * np.exp(-(x - mu) ** 2/(2. * sigma ** 2))

parser = argparse.ArgumentParser(description='Fit gaussian curves to the distribution.')
parser.add_argument('filenames', type=argparse.FileType('r'), nargs='+')
parser.add_argument('-i', '--iterations', nargs='+')
parser.add_argument('-f', '--fit', action='store_true')
args = parser.parse_args()

iterations_used = [int(i) for i in args.iterations]

filenames = [file.name for file in args.filenames]

root_path = getRootDirectory()

for file in filenames:
	full_path = (root_path / file)
	if not full_path.exists() or full_path.is_dir():
		continue

	relative_path = full_path.relative_to(root_path / 'data')

	print('[Gauss] Computing file %s ... ' %relative_path, end='')

	data = {}

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
	min_ = 100
	max_ = -100

	for iteration in iterations_used:
		min_ = min(min_, min(data[iteration - 1]))
		max_ = max(max_, max(data[iteration - 1]))

	bins = np.linspace(min_, max_, 100)	# 100 bins
	for iteration in iterations_used:
		color_plot, color_fit = next(color_iterator)['color']
		hits = np.histogram(data[iteration - 1], bins)[0]
		bins_mid = (bins[1:] + bins[:-1]) / 2
		plt.errorbar(bins_mid, hits, label='path after %d iteration%s' %(iteration, 's' if iteration > 1 else ''), fmt='.', color=color_plot)

		if args.fit:
			try:
				parameters, parameters_error = op.curve_fit(gauss, bins_mid, hits, p0=[1, 1, 1])
				parameters_error = np.sqrt(np.diag(parameters_error))
				xdata_fit = np.linspace(min(bins), max(bins), 1000)
				ydata_fit = gauss(xdata_fit, *parameters)
				plt.plot(xdata_fit, ydata_fit, color=color_fit)
			except:
				pass

	plt.xlabel('Position')
	plt.ylabel('Number')
	plt.legend()

	out_filename = root_path / 'imgs' / relative_path
	out_filename.parent.mkdir(parents=True, exist_ok=True)

	out_filename = out_filename.with_suffix('')
	out_filename = '%s_gauss_%s' %(out_filename, '-'.join([str(i) for i in iterations_used]))

	plt.savefig(out_filename + '.png')
	print('done')
	#plt.savefig(out_filename + '.pdf')