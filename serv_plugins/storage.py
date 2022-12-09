class pages:
	class link:
		main = '/'
		api = '/api'
		open_source = '/os'
	class page:
		main = 'main.html'
		api = 'api.html'
		open_source = 'os.html'

def isnull(obj:str) -> bool:
	if not isinstance(obj, str):
		return False
	if obj.lower() == 'null':
		return True
	return False