# include <fstream>
# include <string>
using namespace std;

# ifdef __cplusplus
extern "C" {
# endif

auto slurp(string path) -> string {
	constexpr auto read_size = size_t(4096);
	auto stream = ifstream(path.data());
	stream.exceptions(ios_base::badbit);
	
	auto out = string();
	auto buf = string(read_size, '\0');
	while (stream.read(& buf[0], read_size)) {
		out.append(buf, 0, stream.gcount());
	}
	out.append(buf, 0, stream.gcount());
	return out;
}

auto get(char* fname) {
	// char* re = new char(fname);
	string filename (*fname, 10);
	ifstream file;
	file.open(filename);
	if (file.is_open()){
		string all_lines = slurp(filename);
		file.close();
		return all_lines;
	} else {
		file.close();
	}
}

int main() { return 0; }

# ifdef __cplusplus
}
# endif