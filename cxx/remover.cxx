# include <string>
# include <stdio.h>
using namespace std;

void deleter(string filename) {
	remove(filename.c_str());
}