from os import listdir, rename
from sys import platform

if platform in ['linux', 'linux2']:
	endl = '.so'
elif platform in ['win32', 'cygwin', 'msys']:
	endl = '.dll'

def main():
	for file in (listdir()):
		if file.endswith(endl):
			rename(file, f"{file.split('.', 1)[0]}{endl}")

if __name__ == '__main__':
	main()