import asyncio
import warnings

from os.path import join
from random import randint
from argparse import ArgumentParser
from aiohttp.web import Application, RouteTableDef, run_app, Response, HTTPFound, json_response
from serv_plugins.binder import Binder
from serv_plugins.database import database
from serv_plugins.face_classifier.tensorBinder import face_rec, TextRecognizer

warnings.filterwarnings('ignore')

app = Application()
routes = RouteTableDef()
binder = Binder()
parser = ArgumentParser(description = 'Project argument')
recognizer = TextRecognizer()

parser.add_argument('--host', help='Host to listen', default='localhost')
parser.add_argument('--port', help='Port for accept connection', default='9000')

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

@routes.post('/api/recognition')
async def api_post_recognition(request):
	try: data = await request.json()
	except Exception as ex: return Response(status=415, body=str(ex))

	try:
		if (await database.exists_token(data['token'])):
			filename = f'{data["token"]}_{randint(1000, 9999)}.png'
			path = await binder.save_photo(data['photo'], filename)
			await face_rec(path)
			new_photo = await binder.get_photo(path)
			return Response(body=new_photo)
		else:
			return Response(status=401)
	except KeyError as ex:
		return Response(status=406, body=str(ex))

@routes.post('/api/text')
async def api_post_text_recognition(request):
	try: data = await request.json()
	except Exception as ex: return Response(status=415, body=str(ex))

	try:
		if (await database.exists_token(data['token'])):
			filename = f'{data["token"]}_{randint(1000, 9999)}.png'
			path = await binder.save_photo(data['photo'], filename)
			airesp = await recognizer.recognition(path)
			return json_response(data={'text': airesp})
		else:
			return Response(status=401)
	except KeyError as ex:
		return Response(status=406, body=str(ex))

@routes.get('/api/all')
async def api_get_all_methods(request):
	return json_response(data={'all': [
		['/api/recognition', 'POST'],
		['/api/text', 'POST'],
		['/api/all', 'GET'],
		['/api/open', 'GET'],
		['/api/links', 'GET'],
		['/api/balance', 'POST']
	]})

@routes.get('/api/open')
async def api_get_open_source(request):
	self_file = await binder.get_open_source()
	return json_response(data={'response': {'open': self_file}})

@routes.get('/api/links')
async def api_get_all_links(request):
	return json_response(data={'all': [
		['github', 'https://github.com/YakovSava/raw_bot_face_recognition'],
		['vk', 'https://vk.me/face_bot_indproj'],
		['tg', 'https://t.me/face_rrecognition_bot']
	]})

@routes.post('/api/balance')
async def api_get_balance(request):
	try: data = await request.json()
	except Exception as ex: return Response(status=415, body=str(ex))

	try:
		if (await database.exists_token(data['token'])):
			id_ = await database.get_from_token(data['token'])
			info = await database.get(id_)
			return json_response(data={
				'id': id_,
				'quantity': info['quantity'],
				'balance': info['balance']
			})
		else: return Response(status=401)
	except KeyError as ex: Response(status=406, body=str(ex))

# Get pages

@routes.get('/')
async def main_page(request):
	some_page = await binder.get_page('index.html')
	if not (some_page):
		raise Response(status=500)
	else:
		return Response(text=some_page, content_type='text/html')

@routes.post('/api')
async def api_page(request):
	page = await binder.get_page('api.html')
	if not (page):
		raise Response(status=500)
	else:
		return Response(text=page, content_type='text/html')

@routes.get('/api')
async def api_page_get(request):
	some_page = await binder.get_page('api.html')
	if not (some_page):
		raise Response(status=500)
	else:
		return Response(text=some_page, content_type='text/html')

@routes.get('/github')
async def github_redirect(request):
	raise HTTPFound('https://github.com/YakovSava/raw_bot_face_recognition')

@routes.get('/telegram')
async def telegram_redirect(request):
	raise HTTPFound('https://t.me/face_rrecognition_bot')

@routes.get('/vk')
async def vkontakte_redirect(request):
	raise HTTPFound('https://vk.me/face_bot_indproj')

def runner(loop=asyncio.get_event_loop()):
	args = parser.parse_args()
	app.add_routes(routes)
	run_app(app, host=args.host, port=args.port, loop=loop)

if __name__ == '__main__':
	runner()