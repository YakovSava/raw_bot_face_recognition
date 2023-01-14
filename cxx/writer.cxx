# include <fstream>
# include <string>
using namespace std;

# ifdef __cplusplus
extern "C" {
# endif

int write(char* fname, char* alll) {
	string filename (fname, 10);
	string all_lines (alll, 10);
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
}

int main() { return 0; }

# ifdef __cplusplus
}
# endif