#include "rand48.h"

/* Initialize the software rand64 implementation.  */
void
software_rand48_init (void)
{
}

/* Return a random value, using software operations.  */
unsigned long long
software_rand48 (void)
{
  struct drand48_data rand_data;
  srand48_r(time(NULL), &rand_data);

  long int res;
  mrand48_r(&rand_data, &res);

  // double the size of the result so the first half of it isn't just zeros
  return ((unsigned long long)res << 32 | ((unsigned long long)res));
}

/* Finalize the software rand48 implementation.  */
void
software_rand48_fini (void)
{
}