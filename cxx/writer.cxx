# include <fstream>
# include <iostream>

# ifdef __cplusplus
extern "C" __declspec(dllexport) {
using namespace std;
# endif

int write(char* filename, char* all_lines) {
	ofstream file;
	file.open(filename);
	cout << "Filename: " << filename << endl;
	cout << "File lines: " << all_lines << endl;
	cout << "Is open: " << file.is_open() << endl;
	if (file.is_open()) {
		file << all_lines << endl;
		file.close();
		return 1;
	} else {
		file.close();
		return 0;
	}
}

# ifdef __cplusplus
}
# endif