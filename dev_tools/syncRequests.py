import requests

from sys import argv

def main():
	with requests.session() as session:
		host = argv[1]
		resp = session.get(host)
		if resp.status == 200:
			resps = [session.get(f'{host}/api/{api}')
				for api in ['all', 'open', 'links']
			]
			for resp in resps:
				resp:requests.Response
				if resp.status == 200:
					print(resp.json())
				else:
					print(resp.status)

			post_resps = [session.post(f'{host}/api/{method}', data=data)
				for method, data in [
					['recognition', {'token': 'dxlvzSMBPc', 'photo': open('test1.png', 'rb').read()}],
					['text', {'token': 'dxlvzSMBPc', 'photo': open('test0.png', 'rb').read()}],
					['balance', {'token': 'dxlvzSMBPc'}]
				]
			]
			for post_resp in post_resps:
				post_resp:requests.Response
				if post_resp.status == 200:
					print(post_resp.json())
				else:
					print(resp.status)

if __name__ == '__main__':
	main()