from os import listdir, rename
from sys import platform
from shutil import copyfile

def main():
	for endl in ['.o', '.dll', '.so']:
		for file in (listdir()):
			if file.endswith(endl):
				rename(file, f"{file.split('.', 1)[0]}{endl}")
				try:
					if platform in ['linux', 'linux2']:
						newend = '.dll'
						copyfile(f"{file.split('.', 1)[0]}{endl}", f"{file.split('.', 1)[0]}{newend}")
					elif platform in ['win32', 'cygwin', 'msys']:
						newend = '.so'
						copyfile(f"{file.split('.', 1)[0]}{endl}", f"{file.split('.', 1)[0]}{newend}")
				except:
					pass

if __name__ == '__main__':
	main()