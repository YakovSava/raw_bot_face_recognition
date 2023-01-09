@echo off

g++ -c -fPIC %1 -o %1.o
g++ -shared -Wl,-soname,%1.dll -o %1.dll  %1.o

echo "Compile succeful!"