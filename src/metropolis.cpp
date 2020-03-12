#include <math.h>
#include <random>
#include "metropolis.h"
#include <chrono>

// returns the value of the potential
double potential(double x, double mu, double lambda)
	{
		return mu * (x * x + lambda * pow(x, 4));
	}

// difference of the energy if x_old is changed to x_new
double delta_energy(double left, double right, double x_new, double x_old, double m, double tau, double mu, double lambda)
	{
		return potential(x_new, mu, lambda) - potential(x_old, mu, lambda) + (m / (tau * tau)) * (x_new * x_new - x_old * x_old - (left + right) * (x_new - x_old));
	}


int accepted = 0;
int total = 0;

// return the accept ratio
double get_accept_ratio(void)
	{
		if (total == 0)
			return 0;
		return (double) accepted / total;
	}

// reset the accept ratio
void reset_ratio(void)
	{
		accepted = 0;
		total = 0;
	}

unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
std::default_random_engine generator(seed);


double * result;

double * metropolis(int num_numbers, double *numbers, double val_width, double m, double tau, double mu, double lambda, double hbar) {
	std::normal_distribution<double> n_distribution(0, val_width);
	std::uniform_real_distribution<double> lin_distribution(0, 1);
    int i;

	// allocate space to fit the result
	result = (double *) malloc(num_numbers * sizeof (double));

    for (i = 0; i < num_numbers; i++) {
		double old_x = numbers[i];
		double new_x = old_x + n_distribution(generator);

		// energy difference
		double d_energy = delta_energy(numbers[i - 1], numbers[(i + 1) % num_numbers], new_x, old_x, m, tau, mu, lambda);

		if (d_energy < 0)
		{
			// accept
			result[i] = new_x;
			accepted ++;
		}
		else
		{
			if (exp(- tau * d_energy / hbar) > lin_distribution(generator))
			{
				// accept
				result[i] = new_x;
				accepted ++;
			}
			else
			{
				// reject
				result[i] = old_x;
			}

		}

    }
	total += num_numbers;
    return result;
}
