# include <fstream>
# include <string>
# include <iostream>
using namespace std;

# ifdef __cplusplus
extern "C" {
# endif

int write(char* fname, char* alll) {
	// string filename (fname, 10);
	string all_lines (alll, 50);
	ofstream file;
	file.open(fname);
	cout << all_lines << fname << endl;
	if (file.is_open()) {
		file << all_lines;
		file.close();
		return 1;
	} else {
		file.close();
		return 0;
	}
}

int main() { return 0; }

# ifdef __cplusplus
}
# endif