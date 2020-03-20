#!/usr/bin/env python3

# import modules
from tools import Potential, Kinetic, Energy, deltaEnergy, Metropolis, getRootDirectory, running_mean, block, autoCorrelationNormalized, getIntegratedCorrelationTime
import numpy as np
from multiprocessing import Pool
import csv
from itertools import islice
from configparser import ConfigParser
import argparse
import pathlib

# parse CLI arguments
parser = argparse.ArgumentParser(description='Create samples for the harmonic oscillator, vary hbar')
parser.add_argument('-i', '--iterations', type=int, default=1000,
                    help='Number of Metropolis iterations')
parser.add_argument('-N', '--number', type=int, default=1000,
                    help='Number of lattice sites')
parser.add_argument('-m', '--mass', type=float, default=0.01,
                    help='Mass of the particle')
parser.add_argument('-u', '--mu', type=float, default=10,
                    help='Depth of the potential')
parser.add_argument('-t', '--tau', type=float, default=0.1,
                    help='Time step size')
parser.add_argument('-hb', '--hbar', type=str, default='0:2:0.05',
                    help='Values of the reduced Plancks constant')
parser.add_argument('-init', '--initial', type=float, default=0,
                    help='Initial values for the path')
parser.add_argument('-ir', '--initial-random', type=float, default=0,
                    help='Use random distribution around initial value')
parser.add_argument('-s', '--step', action='store_true',
                    help='Use a step function as initial state')
parser.add_argument('-o', '--output', type=pathlib.Path,
					help='Output filename')
args = parser.parse_args()


# extract parameters
iterations = args.iterations
N = args.number
mass = args.mass
mu = args.mu
tau = args.tau
hbar_min, hbar_max, hbar_step = (float(h) for h in args.hbar.split(':'))
initial = args.initial
initial_random = args.initial_random
step = args.step
output = args.output

parameters = [
			'N', 'mass', 'mu', 'tau', 'hbar_min', 'hbar_max', 'hbar_step',
			'initial', 'initial_random', 'step',
			]

# filesystem stuff
root_path = getRootDirectory()
dir_ = root_path / 'data' / 'harmonic_oscillator_classical_limit_energy'
dir_.mkdir(exist_ok=True)
file_ = dir_ / ('h%0.2f-%0.2f-%0.4f-N%d.csv' % (hbar_min, hbar_max, hbar_step, N))

if output != None:
	file_ = output

# config output
config_filename = file_.with_suffix('.cfg')
config = ConfigParser()
config['DEFAULT'] = {p: eval(p) for p in parameters}
config['DEFAULT']['type'] = 'harmonic_oscillator_classical_limit_energy'

hbars = np.arange(hbar_min + hbar_step, hbar_max + hbar_step, hbar_step)

def calculateEnergy(hbar):
	print('calculating for hbar=%0.4f' % hbar)
	m = Metropolis(init=initial, valWidth=1, initValWidth=initial_random, hbar=hbar, tau=tau, N=N, m=mass, lambda_=0, mu=mu)

	data = []
	accept_ratios = []
	for _ in range(iterations):
		d, a = m.__next__()
		data.append(d)
		accept_ratios.append(a)

	k = Kinetic(mass, tau)
	p = Potential(mu, 0)
	e = Energy(k, p)
	energies = np.array([e(d) for d in data])

	# calculate mean energy
	d = energies[:-1] - energies[1:]
	da = running_mean(d, 10)
	if da[0] > 0:
		start = np.argmax(da < 0) + 10
	else:
		start = np.argmax(da > 0) + 10

	energies_cut = energies[start:]


	energies_cut_ac = autoCorrelationNormalized(energies_cut, np.arange(len(energies_cut)))

	# calculate integrated autocorrelation time
	tint, dtint, w_max = getIntegratedCorrelationTime(energies_cut_ac, factor=10)

	step_size = int((tint + dtint) * 2 + 1)

	energies_blocked = block(energies_cut, step_size)
	energy, denergy = np.mean(energies_blocked), np.std(energies_blocked)

	return [energy, denergy], np.mean(accept_ratios)

# use a multiprocessing pool to generate data in a parallel manner
#for hbar in np.linspace(0.1, 2.0, 20):
#	print(calculateEnergy(hbar))

p = Pool()
results = p.map(calculateEnergy, hbars)
accept_ratio = np.mean([r[1] for r in results])

# save csv
with file_.open('w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['hbar', 'energy', 'denergy'])
	for i, hbar in enumerate(hbars):
		writer.writerow([hbar] + results[i][0])

config['DEFAULT']['accept_ratio'] = str(accept_ratio)

with open(config_filename, 'w') as configfile:
	config.write(configfile)