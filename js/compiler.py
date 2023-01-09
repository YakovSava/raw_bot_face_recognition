from os import listdir
from Naked.toolshed.shell import muterun_js

class JavaScriptCompiler:

	def __init__(self):
		self.json_path = 'js/json/'
		self.all_js_file = {}
		for file in (listdir('js/')):
			if file.endswith('.js'):
				self.all_js_file[file.split('.')[0]] = file

	async def run(self, name:str) -> bytes:
		response = muterun_js(self.all_js_file[name])
		if response.exitcode == 0:
			return response.stdout
		else:
			return f'Error: {response.stderr}'.encode()

	def run_sync(self, name:str):
		response = muterun_js(self.all_js_file[name])
		if response.exitcode == 0:
			return response.stdout
		else:
			return f'Error: {response.stderr}'.encode()