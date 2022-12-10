import http.client as client

def self_ip():
	conn = client.HTTPConnection("ifconfig.me")
	conn.request("GET", "/ip")
	return conn.getresponse().read()[:-1].decode()