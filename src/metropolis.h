#define DLL_EXPORT __declspec(dllexport)

//DLL_EXPORT double threshIt(double pix, double colors);


#if defined _WIN32 || defined __CYGWIN__ || defined __MINGW32__
    #ifdef BUILDING_DLL
        #ifdef __GNUC__
            #define DLL_PUBLIC __attribute__ ((dllexport))
        #else
            #define DLL_PUBLIC __declspec(dllexport) // Note: actually gcc seems to also supports this syntax.
        #endif
    #else
        #ifdef __GNUC__
            #define DLL_PUBLIC __attribute__ ((dllimport))
        #else
            #define DLL_PUBLIC __declspec(dllimport) // Note: actually gcc seems to also supports this syntax.
        #endif
    #endif
    #define DLL_LOCAL
#else
    #if __GNUC__ >= 4
        #define DLL_PUBLIC __attribute__ ((visibility ("default")))
        #define DLL_LOCAL  __attribute__ ((visibility ("hidden")))
    #else
        #define DLL_PUBLIC
        #define DLL_LOCAL
    #endif
#endif

extern "C" DLL_PUBLIC double get_accept_ratio(void);
extern "C" DLL_PUBLIC void reset_ratio(void);
extern "C" DLL_PUBLIC double * metropolis(int num_numbers, double *numbers, double val_width, double m, double tau, double mu, double lambda, double hbar, bool periodic);
