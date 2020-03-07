from tools import Potential, Kinetic, deltaEnergy, Metropolis, getRootDirectory, distanceToParameter
import os
import numpy as np
from multiprocessing import Pool
import csv
from itertools import islice
from configparser import ConfigParser
import argparse
import pathlib

parser = argparse.ArgumentParser(description='Create samples for the harmonic oscillator, vary hbar')
parser.add_argument("-i", "--iteration", type=int, default=100,
                    help="Number of Metropolis iteration used")
parser.add_argument("-N", "--number", type=int, default=100,
                    help="Number of lattice sites")
parser.add_argument("-m", "--mass", type=float, default=0.01,
                    help="Mass of the particle")
parser.add_argument("-u", "--mu", type=float, default=10,
                    help="Depth of the potential")
parser.add_argument("-t", "--tau", type=float, default=0.1,
                    help="Time step size")
parser.add_argument("-hb", "--hbar", type=float, default=1,
                    help="Values of the reduces Plancks constant")
parser.add_argument("-b", "--bins", type=str, default='-5:5:0.1',
                    help="Range of the used bins")
parser.add_argument("-init", "--initial", type=float, default=0,
                    help="Initial values for the path")
parser.add_argument("-ir", "--initial-random", type=float, default=0,
                    help="Use random distribution around initial value")
parser.add_argument("-s", "--step", action='store_true',
                    help="Use a step function as initial state")
parser.add_argument("-d", "--distance", type=str, default='0:10:0.1',
                    help="Distance of the minima")
parser.add_argument('-o', '--output', type=pathlib.Path,
					help="Output filename")
args = parser.parse_args()

# parameters
iteration = args.iteration
N = args.number
mass = args.mass
mu = args.mu
tau = args.tau
hbar = args.hbar
bins_min, bins_max, bins_step = (float(b) for b in args.bins.split(':'))
initial = args.initial
initial_random = args.initial_random
step = args.step
distance_min, distance_max, distance_step = (float(d) for d in args.distance.split(':'))
output = args.output

parameters = [
			'iteration', 'N', 'mass', 'mu', 'tau', 'hbar',
			'bins_min', 'bins_max',	'bins_step',
			'initial', 'initial_random', 'step',
			'distance_min', 'distance_max', 'distance_step',
			]

root_path = getRootDirectory()
dir_ = root_path / 'data' / 'anharmonic_oscillator_lambda_parameter'
dir_.mkdir(exist_ok=True)
file_ = dir_ / ('d%0.2f-%0.2f-%0.2fs%0.2f-%0.2f-%0.2f-N%d-i%d.csv' % (distance_min, distance_max, distance_step, bins_min, bins_max, bins_step, N, iteration))

if output != None:
	file_ = output

config_filename = file_.with_suffix('.cfg')
config = ConfigParser()
config['DEFAULT'] = {p: eval(p) for p in parameters}
config['DEFAULT']['type'] = 'anharmonic_oscillator_lambda_parameter'

distances = np.arange(distance_min + distance_step, distance_max + distance_step, distance_step)
bins = np.arange(bins_min, bins_max + bins_step, bins_step)

def calculatePositionDistribution(distance):
	print("calculating for distance=%0.2f" % distance)
	lambda_ = distanceToParameter(distance)
	p = Potential(-mu, lambda_)

	de = deltaEnergy(p, mass, tau)

	m = Metropolis(de, init=initial, valWidth=1, initValWidth=initial_random, hbar=hbar, tau=tau, N=N)

	vals = next(islice(m, iteration, iteration + 1))			# get iterations th metropolis iteration
	return list(np.histogram(vals[0], bins)[0]), vals[1]

p = Pool()
results = p.map(calculatePositionDistribution, distances)
accept_ratio = np.mean([r[1] for r in results])

with file_.open('w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['distance'] + list(bins[:-1]))
	writer.writerow(['distance'] + list(bins[1:]))
	for i, distance in enumerate(distances):
		writer.writerow([distance] + results[i][0])

config['DEFAULT']['accept_ratio'] = str(accept_ratio)

with open(config_filename, 'w') as configfile:
	config.write(configfile)