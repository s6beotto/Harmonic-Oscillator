from matplotlib import pyplot as plt
from tools import Potential, distanceToParameter
import numpy as np

# number of distances evaluated
min_distance = 1
max_distance = 16
step_distance = 1

params = [
	(10, 0, 'harm', 0)
]

distances = np.arange(min_distance, max_distance, step_distance)

params += [
	(-10, distanceToParameter(d), 'anharm: %0.2f' %d, d) for d in distances
]

for mu, lambda_, name, d in params:
	xvalues = np.arange(-5-d / 2, 5+d / 2, 0.01)
	p = Potential(mu, lambda_)
	yvalues = p(xvalues)
	plt.figure()
	plt.errorbar(xvalues, yvalues)
	plt.xlabel('Distance')
	plt.ylabel('Tunneling rate')
	plt.savefig('imgs/d_%s.pdf' %name)
	plt.close()