# include <fstream>
# include <string>
using namespace std;

int write(string filename, string lines) {
	ofstream file;
	file.open(filename.c_str());
	if (file.is_open()) {
		file << lines << endl;
		file.close();
		return 1;
	} else {
		file.close();
		return 0;
	}
}