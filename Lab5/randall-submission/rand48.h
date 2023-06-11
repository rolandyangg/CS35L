#ifndef rand48_h
#define rand48_h

#include <stdlib.h>

void
software_rand48_init(void);

unsigned long long
software_rand48(void);

void
software_rand48_fini(void);

#endif /* rand48_h */