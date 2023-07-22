#pragma once
#define DLL_TEST64_EXPORTS
#ifdef DLL_TEST64_EXPORTS
#define DLL_TEST64_API __declspec(dllexport)
#else
#define DLL_TEST64_API __declspec(dllimport)
#endif

extern "C" DLL_TEST64_API void DLL_TEST1();
extern "C" DLL_TEST64_API int ADD(int a, int b);
extern "C" DLL_TEST64_API int test_ptr(int* a, int b);
extern "C" DLL_TEST64_API int test_ptr_ptr(int** a, int b);
extern "C" DLL_TEST64_API int test_ptr_test(int* a, int b);
