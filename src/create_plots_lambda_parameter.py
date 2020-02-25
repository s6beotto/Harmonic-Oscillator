from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import sys
from tools import getRootDirectory
import csv


import argparse
from glob import glob

import itertools
flatten = itertools.chain.from_iterable

parser = argparse.ArgumentParser(description='Fit gaussian curves to the distribution.')
parser.add_argument('filenames', nargs='*')
args = parser.parse_args()
root_path = getRootDirectory()

filenames = list(flatten([glob(arg) for arg in args.filenames]))

root_path = getRootDirectory()

for file in filenames:
	full_path = (root_path / file)
	if not full_path.exists() or full_path.is_dir():
		continue

	relative_path = full_path.relative_to(root_path / 'data')

	print('[Lambda parameter] Computing file %s ... ' %relative_path, end='')

	with full_path.open('r') as csvfile:
		reader = csv.reader(csvfile)
		distances = []
		datas = []
		for i, row in enumerate(reader):
			if i == 0:
				header_min = [float(v) for v in row[1:]]
			elif i == 1:
				header_max = [float(v) for v in row[1:]]
			else:
				distance = float(row[0])
				data = [int(v) for v in row[1:]]
				distances.append(distance)
				datas.append(data)


	fig, ax = plt.subplots(figsize=(6,6))
	cs = ax.imshow(datas, extent=[min(header_min), max(header_max), max(distances), min(distances)], norm=LogNorm())

	cbar = fig.colorbar(cs)
	cbar.ax.minorticks_off()

	plt.plot([+d / 2 for d in distances], distances, color='black', label='Classical Minima')
	plt.plot([-d / 2 for d in distances], distances, color='black')

	x0,x1 = ax.get_xlim()
	y0,y1 = ax.get_ylim()
	ax.set_aspect(abs(x1-x0)/abs(y1-y0))

	plt.xlabel('position')
	plt.ylabel('minima distance')

	plt.legend()

	out_filename = root_path / 'imgs' / relative_path
	out_filename.parent.mkdir(parents=True, exist_ok=True)

	out_filename = out_filename.with_suffix('')
	out_filename = '%s_lambda' %(out_filename)

	plt.savefig(out_filename + '.png')
	print('done')