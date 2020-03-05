from matplotlib import pyplot as plt
from tools import getRootDirectory
import csv
import numpy as np

import argparse
from glob import glob

import itertools
flatten = itertools.chain.from_iterable

parser = argparse.ArgumentParser(description='Plot the path of a particle at different metropolis states shifted.')
parser.add_argument('filenames', type=argparse.FileType('r'), nargs='+')
parser.add_argument('-i', "--iterations", nargs='+')
args = parser.parse_args()

iterations_used = args.iterations

filenames = [file.name for file in args.filenames]

root_path = getRootDirectory()

for file in filenames:
	full_path = (root_path / file)
	if not full_path.exists() or full_path.is_dir():
		continue

	relative_path = full_path.relative_to(root_path / 'data')

	print("[Track shifted] Computing file %s ... " %relative_path, end='')

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
	sep = 0.5
	for num, iteration in enumerate(iterations_used):
		iteration = int(iteration)
		plt.errorbar(numbers, data[iteration - 1] - num, label='path after %d iteration%s' %(iteration, 's' if iteration > 1 else ''))
		plt.xlabel('Number')
		plt.ylabel('Position $- 0.5 \cdot n$')
	plt.legend()

	out_filename = root_path / 'imgs' / relative_path
	out_filename.parent.mkdir(parents=True, exist_ok=True)

	out_filename = out_filename.with_suffix('')
	out_filename = '%s_track_shifted_%s' %(out_filename, '-'.join([str(i) for i in iterations_used]))

	plt.savefig(out_filename + '.png')
	print('done')
	#plt.savefig(out_filename.with_suffix(".pdf"))