import asyncio
import warnings

from aiohttp.web import Application, RouteTableDef, HTTPInternalServerError, run_app, Response, HTTPFound
from argparse import ArgumentParser
from sys import platform
from serv_plugins.storage import isnull
from serv_plugins.binder import Binder

warnings.filterwarnings('ignore')

if platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

app = Application()
routes = RouteTableDef()
binder = Binder()
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

# Get pages

@routes.get('/')
async def main_page(request):
	some_page = await binder.get_page('index.html')
	if isnull(some_page):
		raise HTTPInternalServerError()
	else:
		return Response(text = some_page, content_type='text/html')

@routes.post('/api')
async def api_page(request):
	page = await binder.get_page('api.html')
	if isnull(page):
		raise HTTPInternalServerError()
	else:
		return Response(text = page, content_type='text/html')

@routes.get('/api')
async def api_page_get(request):
	some_page = await binder.get_page('api.html')
	if isnull(some_page):
		raise HTTPInternalServerError()
	else:
		return Response(text = some_page, content_type='text/html')

@routes.get('/github')
async def github_redirect(request):
	raise HTTPFound('https://github.com/YakovSava/raw_bot_face_recognition')

@routes.get('/telegram')
async def telegram_redirect(request):
	# Redirect
	...

@routes.get('/vk')
async def vkontakte_redirect(request):
	# Redirect
	...


if __name__ == '__main__':
	args = parser.parse_args()
	app.add_routes(routes)
	try:
		run_app(app, host = args.host, port = args.port)
	except OSError as err:
		print(f'Error with host/port - {err}')