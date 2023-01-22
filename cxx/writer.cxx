# include <fstream>
using namespace std;

extern "C" __declspec(dllexport)
int write(const char* filename, const char* all_lines) {
	ofstream file;
	file.open(filename, ios::out);
	if (file.is_open()) {
		file << "What" << endl;
		return 0;
	} else {
		return 1;
	}
}

extern "C" __declspec(dllexport)
int main() { write("file.txt", "help"); return 0; }