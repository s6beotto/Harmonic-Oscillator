from matplotlib import pyplot as plt
import matplotlib
from tools import getRootDirectory, getColorIterator
import csv
import numpy as np
import scipy.optimize as op
#import scipy.stats as stats
import statsmodels.api as sm
import argparse
from glob import glob

import itertools
flatten = itertools.chain.from_iterable

color_iterator = getColorIterator()


parser = argparse.ArgumentParser(description='Check distribution via a qq plot.')
parser.add_argument('filenames', type=argparse.FileType('r'), nargs='+')
parser.add_argument('-i', '--iteration', type=int, default=1)
args = parser.parse_args()

iteration = args.iteration

filenames = [file.name for file in args.filenames]

root_path = getRootDirectory()

for file in filenames:
	full_path = (root_path / file)
	if not full_path.exists() or full_path.is_dir():
		continue

	relative_path = full_path.relative_to(root_path / 'data')

	print('[QQ] Computing file %s ... ' %relative_path, end='')

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

	d = data[iteration - 1]

	#stats.probplot(d, dist="norm", plot=plt) #, plottype='qq'
	sm.qqplot(d, dist='norm')

	out_filename = root_path / 'imgs' / relative_path
	out_filename.parent.mkdir(parents=True, exist_ok=True)

	out_filename = out_filename.with_suffix('')
	out_filename = '%s_qq_%d' %(out_filename, iteration)

	plt.savefig(out_filename + '.png')
	print('done')
	#plt.savefig(out_filename + '.pdf')