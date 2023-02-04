import asyncio
import warnings

from argparse import ArgumentParser
from sys import platform
from aiohttp.web import Application, RouteTableDef, HTTPInternalServerError, run_app, Response, HTTPFound, json_response
from serv_plugins.binder import Binder
from serv_plugins.random_generator import Generator
from serv_plugins.utils import exists,exists_key

warnings.filterwarnings('ignore')

if platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

app = Application()
routes = RouteTableDef()
binder = Binder()
gen = Generator()
parser = ArgumentParser(description = 'Project argument')

parser.add_argument('--host', help = 'Host to listen', default = 'localhost')
parser.add_argument('--port', help = 'Port for accept connection', default = '9000')

# Get images, CSS and more

@routes.get('/styles/style.css')
async def server_get_style(request):
	css_text = await binder.get_page('styles/style.css')
	return Response(
		text=css_text,
		content_type='text/css'
	)

@routes.get('/images/logot.ico')
async def server_get_logo(request):
	photo = await binder.server_get_photo('images/logot.ico')
	return Response(
		body=photo,
		content_type='image/x-icon'
	)

@routes.get('/images/example__img_before.png')
async def server_get_example__img_before(request):
	photo = await binder.server_get_photo('images/example__img_before.png')
	return Response(
		body=photo,
		content_type='image/png'
	)

@routes.get('/images/example__img_after.png')
async def server_get_example__img_after(request):
	photo = await binder.server_get_photo('images/example__img_after.png')
	return Response(
		body=photo,
		content_type='image/png'
	)

@routes.get('/images/example__img_arrow.svg')
async def server_get_example__img_arrow(request):
	photo = await binder.server_get_photo('images/example__img_arrow.svg')
	return Response(
		body=photo,
		content_type='image/svg+xml'
	)

@routes.get('/images/mag-glass.png')
async def server_getmag_glass(request):
	photo = await binder.server_get_photo('images/mag-glass.png')
	return Response(
		body=photo,
		content_type='image/png'
	)

@routes.get('/images/egg.png')
async def server_get_egg(request):
	photo = await binder.server_get_photo('images/egg.png')
	return Response(
		body=photo,
		content_type='image/png'
	)

@routes.get('/api-styles/style.css')
async def server_api_get_style(request):
	style = await binder.get_page('api-styles/style.css')
	return Response(
		text=style,
		content_type='text/css'
	)

@routes.get('/images/proc.png')
async def server_get_proc(request):
	photo = await binder.server_get_photo('images/proc.png')
	return Response(
		body=photo,
		content_type='image/png'
	)

@routes.get('/scripts/script.js')
async def server_get_scripts(request):
	script_text = await binder.get_page('scripts/script.js')
	return Response(
		text=script_text,
		content_type='text/javascript'
	)

# Api

@routes.get('/api/recognition')
async def api_get_recognition(request):
	return json_response(data={'response': {'error': 1, 'description': 'Not GET, POST!'}})

@routes.post('/api/recognition')
async def api_post_recognition(request, data:dict):
	if exists(data):
		key = await gen.get()
		if (await binder.save_photo(data['image'], f'{key}.png')):
			return json_response(data={'response': {'key': key}})
		return json_response(data={'response': {'error': 3, 'description': 'This is not photo'}})
	return json_response(data={'response': {'error': 2, 'description': 'File not found'}})

@routes.get('/api/text')
async def api_get_text_recognition(request):
	return json_response(data={'response': {'error': 1, 'description': 'Not GET, POST!'}})

@routes.post('/api/text')
async def api_post_text_recognition(request):
	raise NotImplemented

@routes.get('/api/all')
async def api_get_all_methods(request):
	return json_response(data={'response': {'all': [
		['/api/recognition', 'POST'],
		['/api/text', 'POST'],
		['/api/all', 'GET'],
		['/api/open', 'GET'],
		['/api/links', 'GET'],
		['/api/recognition/put', 'PUT'],
		['/api/recognition/delete', 'DELETE']
	]}})

@routes.get('/api/open')
async def api_get_open_source(request):
	self_file = await binder.get_open_source()
	return json_response(data={'response': {'open': self_file}})

@routes.get('/api/links')
async def api_get_all_links(request):
	return json_response(data={'response': {'all': [
		['github', 'https://github.com/YakovSava/raw_bot_face_recognition'],
		['vk', ''],
		['tg', ''],
		['site', '']
	]}})

@routes.put('/api/recognition/put')
async def api_recognition_put(request, data:dict):
	if exists_key(data):
		key = data['key']
		if (await gen.check(key)):
			try:
				ai_data = await binder.get_photo(f'{key}.png')
			except:
				return json_response(data={'response': {'error': 2, 'description': 'File not found'}})
			return json_response(data={'response': {'image': ai_data, 'key': key}})
		return json_response(data={'response': {'error': 4, 'description': 'Key not exists'}})
	return json_response(data={'response': {'error': 5, 'description': 'Key not found'}})

@routes.delete('/api/recognition/delete')
async def api_recognition_delete(request, data:dict):
	if exists_key(data):
		key = data['key']
		if (await gen.check(key)):
			await binder.delete_photo(f'{key}.png')
			await gen.delete(key)
			return json_response(data={'response': {'succes': 1}})
		return json_response(data={'response': {'error': 4, 'description': 'Key not exists'}})
	return json_response(data={'response': {'error': 5, 'description': 'Key not found'}})


# Get pages

@routes.get('/')
async def main_page(request):
	some_page = await binder.get_page('index.html')
	if not (some_page):
		raise HTTPInternalServerError()
	else:
		return Response(text = some_page, content_type='text/html')

@routes.post('/api')
async def api_page(request):
	page = await binder.get_page('api.html')
	if not (page):
		raise HTTPInternalServerError()
	else:
		return Response(text = page, content_type='text/html')

@routes.get('/api')
async def api_page_get(request):
	some_page = await binder.get_page('api.html')
	if not (some_page):
		raise HTTPInternalServerError()
	else:
		return Response(text = some_page, content_type='text/html')

@routes.get('/github')
async def github_redirect(request):
	raise HTTPFound('https://github.com/YakovSava/raw_bot_face_recognition')

@routes.get('/telegram')
async def telegram_redirect(request):
	raise HTTPFound('https://t.me/face_rrecognition_bot')

@routes.get('/vk')
async def vkontakte_redirect(request):
	# Redirect
	...

def runner(loop=asyncio.get_event_loop()):
	args = parser.parse_args()
	app.add_routes(routes)
	run_app(app, host=args.host, port=args.port, loop=loop)

if __name__ == '__main__':
	runner()