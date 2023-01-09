echo "Start compile .so file!"

g++ -c -fPIC $0 -o $0.o
g++ -shared -Wl,-soname,$0.so -o $0.so  $0.o

echo "Compile succeful!"