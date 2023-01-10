def exists(data:dict) -> bool:
	try:
		data['image']
	except:
		return False
	else:
		return True

def exists_key(data:dict) -> bool:
	try:
		data['key']
	except:
		return False
	else:
		return True