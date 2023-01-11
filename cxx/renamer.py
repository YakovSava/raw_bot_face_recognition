from os import listdir, rename

def main():
	for endl in ['.dll', '.so', '.o']:
		for file in (listdir()):
			if file.endswith(endl):
				rename(file, f"{file.split('.', 1)[0]}{endl}")

if __name__ == '__main__':
	main()