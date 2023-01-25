import requests

from sys import argv

def main():
	with requests.session() as session:
		for _ in range(5): session.get(argv[1])

if __name__ == '__main__':
	main()