# include <fstream>
using namespace std;

extern "C" __declspec(dllexport) int write(char *filename, char *lines) {
	ofstream file;
	file.open(filename);
	if (file.is_open()) {
		file << lines << endl;
		file.close();
		return 1;
	} else {
		file.close();
		return 0;
	}
}