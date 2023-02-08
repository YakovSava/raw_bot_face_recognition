@echo off

clang++ -c -o %1.o %1.cxx
clang++ -shared -v -o %1.dll %1.o
mkdir tmp/
copy %1.dll tmp/
rename tmp/%1.dll tmp/%1.so
move tmp/%1.so %cd%
rmdir /s /q tmp

echo "Compile succeful!"