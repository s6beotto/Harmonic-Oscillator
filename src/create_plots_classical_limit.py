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
parser.add_argument('filenames', type=argparse.FileType('r'), nargs='+')
args = parser.parse_args()
root_path = getRootDirectory()

filenames = [file.name for file in args.filenames]

root_path = getRootDirectory()

for file in filenames:
	full_path = (root_path / file)
	if not full_path.exists() or full_path.is_dir():
		continue

	relative_path = full_path.relative_to(root_path / 'data')

	print('[Classical limit] Computing file %s ... ' %relative_path, end='')

	with full_path.open('r') as csvfile:
		reader = csv.reader(csvfile)
		hbars = []
		datas = []
		for i, row in enumerate(reader):
			if i == 0:
				header_min = [float(v) for v in row[1:]]
			elif i == 1:
				header_max = [float(v) for v in row[1:]]
			else:
				hbar = float(row[0])
				data = [int(v) for v in row[1:]]
				hbars.append(hbar)
				datas.append(data)


	fig, ax = plt.subplots(figsize=(6,6))
	cs = ax.imshow(datas, extent=[min(header_min), max(header_max), max(hbars), min(hbars)], norm=LogNorm())

	cbar = fig.colorbar(cs)
	cbar.ax.minorticks_off()

	x0, x1 = ax.get_xlim()
	y0, y1 = ax.get_ylim()
	ax.set_aspect(abs(x1-x0)/abs(y1-y0))

	plt.xlabel('position')
	plt.ylabel('$\\hbar$')

	out_filename = root_path / 'imgs' / relative_path
	out_filename.parent.mkdir(parents=True, exist_ok=True)

	out_filename = out_filename.with_suffix('')
	out_filename = '%s_classical' %(out_filename)

	plt.savefig(out_filename + '.png')
	print('done')