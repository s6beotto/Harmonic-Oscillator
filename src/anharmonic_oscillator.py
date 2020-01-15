from tools import Potential, Action, Metropolis
from matplotlib import pyplot as plt

# number of lattice positions
N = 1000

# parameters
mass = 0.01
mu = -10
lambda_ = -0.02
initval = -5

tau = 0.1

p = Potential(mu, lambda_)

a = Action(tau, mass, p)

m = Metropolis(N, a, borders = [-10, 10], initval=initval)

vals = list(m)

plt.plot()
plt.errorbar(vals, range(N))
plt.xlim(*m.borders)
plt.show()

plt.figure()
plt.hist(vals, bins = 40)
plt.xlim(*m.borders)
plt.show()