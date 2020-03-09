from matplotlib import pyplot as plt
from tools import getRootDirectory, Energy, Kinetic, Potential, bootstrap
import csv
import numpy as np

import argparse
import pathlib
import configparser


parser = argparse.ArgumentParser(description='Plot the path of a particle at different metropolis states.')
parser.add_argument('filename', type=pathlib.Path, help="Input filename")
parser.add_argument('-i', '--max_iteration', type=int)
parser.add_argument('-l', '--log', action='store_true')
parser.add_argument('-o', '--output', type=pathlib.Path, help="Output filename")
args = parser.parse_args()

root_path = getRootDirectory()
max_iteration = args.max_iteration


full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print("[Track] Computing file %s ... " %relative_path, end='')

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

config = configparser.ConfigParser()
config.read(full_path.with_suffix('.cfg'))


# read config from respective file
m = config['DEFAULT'].getfloat('mass', fallback=1.0)
tau = config['DEFAULT'].getfloat('tau', fallback=1.0)
mu = config['DEFAULT'].getfloat('mu', fallback=1.0)
lambda_ = config['DEFAULT'].getfloat('lambda_', fallback=0)


xdata = list(data.keys())

k = Kinetic(m, tau)

p = Potential(mu, lambda_)

e = Energy(k, p)
ydata = np.array([e(data[x]) for x in xdata])

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)

d = ydata[:-1] - ydata[1:]
da = running_mean(d, 10)
if da[0] > 0:
	start = np.argmax(da < 0) + 10
else:
	start = np.argmax(da > 0) + 10

to_use = ydata[start:]


bootstrap_values = bootstrap(1000, to_use)

energy, denergy = np.mean(bootstrap_values), np.std(bootstrap_values)


plt.errorbar(xdata[:max_iteration], ydata[:max_iteration], label=r'energy $\bar{E} = (%.2f \pm %.2f) \cdot 10^3$' %(energy / 1000, denergy / 1000))
plt.xlabel('Number')
plt.ylabel('Energy')
if args.log:
	plt.yscale('log')
plt.legend()


out_filename = root_path / 'imgs' / relative_path

out_filename = out_filename.with_suffix('')
out_filename = pathlib.Path('%s_thermalisation.pdf' %(out_filename))
if args.output:
	out_filename = args.output
out_filename.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(out_filename)
print('done')