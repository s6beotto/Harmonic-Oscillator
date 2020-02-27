from tools import Potential, Kinetic, deltaEnergy, Metropolis, getRootDirectory, distanceToParameter
import os
import numpy as np
from multiprocessing import Pool
from pathlib import Path
import csv
from itertools import islice
from configparser import ConfigParser

import argparse

parser = argparse.ArgumentParser(description='Create samples for the harmonic oscillator, vary hbar')
parser.add_argument("-i", "--iterations", type=int, default=100,
                    help="Number of Metropolis iterations")
parser.add_argument("-N", "--number", type=int, default=100,
                    help="Number of lattice sites")
parser.add_argument("-m", "--mass", type=float, default=0.01,
                    help="Mass of the particle")
parser.add_argument("-u", "--mu", type=float, default=10,
                    help="Depth of the potential")
parser.add_argument("-t", "--tau", type=float, default=0.1,
                    help="Time step size")
parser.add_argument("-hb", "--hbar", type=str, default='0:2:0.01',
                    help="Values of the reduces Plancks constant")
parser.add_argument("-b", "--bins", type=str, default='-5:5:0.1',
                    help="Range of the used bins")
parser.add_argument("-init", "--initial", type=float, default=0,
                    help="Initial values for the path")
parser.add_argument("-ir", "--initial-random", type=float, default=0,
                    help="Use random distribution around initial value")
parser.add_argument("-s", "--step", action='store_true',
                    help="Use a step function as initial state")
parser.add_argument("-d", "--distance", type=float, default=10,
                    help="Distance of the minima")
parser.add_argument("-o", "--output", type=str, default='',
                    help="Output filename")
args = parser.parse_args()

# parameters
iterations = args.iterations
N = args.number
mass = args.mass
mu = args.mu
tau = args.tau
hbar_min, hbar_max, hbar_step = (float(h) for h in args.hbar.split(':'))
bins_min, bins_max, bins_step = (float(b) for b in args.bins.split(':'))
initial = args.initial
initial_random = args.initial_random
step = args.step
distance = args.distance
lambda_ = distanceToParameter(distance)
output = args.output

parameters = [
			'iterations', 'N', 'mass', 'mu', 'tau', 'hbar_min', 'hbar_max', 'hbar_step',
			'bins_min', 'bins_max', 'bins_step', 'initial', 'initial_random', 'step',
			'distance', 'lambda_',
			]

root_path = getRootDirectory()
dir_ = root_path / 'data' / 'anharmonic_oscillator_classical_limit'
dir_.mkdir(exist_ok=True)
file_ = dir_ / ('h%0.2f-%0.2f-%0.4f_%0.2f-%0.2f-%0.2f-N%dd%0.4f.csv' % (hbar_min, hbar_max, hbar_step, bins_min, bins_max, bins_step, N, distance))
if output != '':
	file_ = dir_ / output
config_filename = file_.with_suffix('.cfg')
config = ConfigParser()
config['DEFAULT'] = {p: eval(p) for p in parameters}
config['DEFAULT']['type'] = 'anharmonic_oscillator_classical_limit'

hbars = np.arange(hbar_min + hbar_step, hbar_max + hbar_step, hbar_step)
bins = np.arange(bins_min, bins_max + bins_step, bins_step)

def calculatePositionDistribution(hbar):
	print("calculating for hbar=%0.4f" % hbar)
	p = Potential(-mu, lambda_)

	k = Kinetic(mass, tau)

	de = deltaEnergy(k, p)

	m = Metropolis(de, init=initial, valWidth=1, initValWidth=initial_random, hbar=hbar, tau=tau, N=N)

	vals = next(islice(m, iterations, iterations + 1))			# get iterations th metropolis iteration
	return list(np.histogram(vals[0], bins)[0]), vals[1]

p = Pool()
results = p.map(calculatePositionDistribution, hbars)
accept_ratio = np.mean([r[1] for r in results])

with file_.open('w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['hbar'] + list(bins[:-1]))
	writer.writerow(['hbar'] + list(bins[1:]))
	for i, hbar in enumerate(hbars):
		writer.writerow([hbar] + results[i][0])

config['DEFAULT']['accept_ratio'] = str(accept_ratio)

with open(config_filename, 'w') as configfile:
	config.write(configfile)