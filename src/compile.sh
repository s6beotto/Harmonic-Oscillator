cd src

g++ -c -fPIC metropolis.cpp -o metropolis.o
g++ -shared -Wl,-soname,libmetropolis.so -o libmetropolis.so  metropolis.o -lm