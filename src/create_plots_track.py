from matplotlib import pyplot as plt
from tools import getRootDirectory
import csv
import numpy as np

import argparse
from glob import glob

import itertools
flatten = itertools.chain.from_iterable

parser = argparse.ArgumentParser(description='Plot the path of a particle at different .')
parser.add_argument("filenames", nargs='*')
parser.add_argument('-i', "--iterations", nargs='+')
args = parser.parse_args()

iterations_used = args.iterations

filenames = list(flatten([glob(arg) for arg in args.filenames]))

root_path = getRootDirectory()

for file in filenames:
	full_path = (root_path / file)
	if not full_path.exists() or full_path.is_dir():
		continue

	relative_path = full_path.relative_to(root_path / 'data')

	print("\nComputing file %s ..." %relative_path)

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
	for iteration in iterations_used:
		iteration = int(iteration)
		plt.errorbar(data[iteration - 1], numbers, label='path after %d iteration%s' %(iteration, 's' if iteration > 1 else ''))
		plt.xlabel('Position')
		plt.ylabel('Number')
	plt.legend()

	out_filename = root_path / 'imgs' / relative_path
	out_filename.parent.mkdir(exist_ok=True)

	plt.savefig(out_filename.with_suffix(".png"))
	plt.savefig(out_filename.with_suffix(".pdf"))