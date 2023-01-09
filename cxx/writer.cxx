# include <fstream>
# include <string>
using namespace std;

extern "C" {int write(string filename, string all_lines) {
	ofstream file;
	file.open(filename, ios::app);
	if (file.is_open()) {
		file << all_lines << endl;
		file.close();
		return 1;
	} else {
		file.close();
		return 0;
	}
}}

int main() { return 0; }