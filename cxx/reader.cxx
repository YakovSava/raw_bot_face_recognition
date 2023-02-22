# include <string>
# include <fstream>
using namespace std;

string concatinate(string first, string second) { 
	string endline = "\n";
	return first + endline +second;
}

string read(string filename) {
	ifstream file(filename.c_str());
	string line, lines = "";

	if (file.is_open()) {
		while (getline(file, line)) {
			lines = concatinate(lines, line);
		}
	} else {
		lines = "bad open";
	}
	file.close();
	return lines;
}