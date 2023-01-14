@echo off

g++ -c -fextended-identifiers -std=c++20 -fPIC %1 -o %1.o
g++ -shared -fextended-identifiers -std=c++20 -Wl,-soname,%1.dll -o %1.dll  %1.o

echo "Compile succeful!"