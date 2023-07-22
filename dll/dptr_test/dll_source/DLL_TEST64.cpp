#include "pch.h" 
#include "python_test.h"
#include <stdio.h>

int gValue = 1000;

void DLL_TEST1()
{
	MessageBox(NULL, TEXT("DLLŒÄ‚Ño‚µ¬Œ÷I"), TEXT("test"), MB_OK);
	Beep(523, 200);
}

int ADD(int a, int b)
{
	return a + b;
}

int test_ptr(int *a, int b)
{

	*a = 0x0201;

	return 0;
}

int test_ptr_ptr(int** a, int b)
{	
	int test = 100;
	*a = &gValue;

	printf("gValue:%d\n", **a);
	printf("gValue:%p\n", &gValue);


	return 0;
}

int test_ptr_test(int* a, int b)
{

	printf("a:%d\n", *a);

	return 0;
}
