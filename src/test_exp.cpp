/* exp example */
#include <stdio.h>      /* printf */
#include <math.h>       /* exp */

int main ()
{
  	double param, result;
  	for (param=-5; param < 5; param = param + 0.1)
		{
		result = exp (param);
		printf ("The exponential value of %f is %f.\n", param, result );
		}
	return 0;
}