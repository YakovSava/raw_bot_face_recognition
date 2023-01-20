# include <fstream>
using namespace std;


extern "C" {
int write(char* filename, char* all_lines) {
	ofstream file;
	file.open(filename);
	if (file.is_open()) {
		file << all_lines << endl;
		file.close();
		return 1;
	} else {
		file.close();
		return 0;
	}
}
}