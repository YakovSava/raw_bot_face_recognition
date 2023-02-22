# include <string>
# include <fstream>
using namespace std;

string concatinate(string first, string second) { return first + second; }

string read(char* filename) {
	string line, lines = "";
	ifstream file;
	file.open(filename);
	if (file.is_open()) {
		while (file >> line) {
			lines = concatinate(lines, line);
		}
	} else {
		lines = "bad open";
	}
	file.close();
	return lines;
}