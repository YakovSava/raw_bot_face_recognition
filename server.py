import asyncio
import warnings

from aiohttp.web import Application, RouteTableDef, HTTPInternalServerError, run_app, Response, 
from argparse import ArgumentParser
from sys import platform
from serv_plugins.storage import isnull
from serv_plugins.binder import Binder

warnings.filterwarnings('ignore')

if platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

app = Application()
routes = RouteTableDef()
binder = Binder()
parser = ArgumentParser(description = 'Project argument')

parser.add_argument('--host', help = 'Host to listen', default = 'localhost')
parser.add_argument('--port', help = 'Port for accept connection', default = '9000')

# Get photos, CSS and more

@routes.get('/styles/style.css')
async def server_get_style(request):
	css_text = await binder.get_page('styles/style.css')
	return Response(
		text=css_text,
		content_type='text/css'
	)

@routes.get('/photos/logot.ico')
async def server_get_logo(request):
	photo = await binder.server_get_photo('photos/logot.ico')
	return Response(
		text=photo,
		content_type='image/x-icon'
	)

@routes.get('/photos/example__img_before.png')
async def server_get_example__img_before(request):
	photo = await binder.server_get_photo('photos/example__img_before.png')
	return Response(
		text=photo,
		content_type='image'
	)

@routes.get('/photos/example__img_after.png')
async def server_get_example__img_after(request):
	photo = await binder.server_get_photo('photos/example__img_after.png')
	return Response(
		text=photo,
		content_type='image'
	)

@routes.get('/photos/example__img_arrow.svg')
async def server_get_example__img_arrow(request):
	photo = await binder.server_get_photo('photos/example__img_arrow.svg')
	return Response(
		text=photo,
		content_type='image'
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
	pass

@routes.get('/api')
async def api_page_get(request):
	some_page = await binder.get_page('api.html')
	if isnull(some_page):
		raise HTTPInternalServerError()
	else:
		return Response(text = some_page, content_type='text/html')

@routes.get('/os')
async def get_open_source(request):
	# Redirect
	...

if __name__ == '__main__':
	args = parser.parse_args()
	app.add_routes(routes)
	try:
		run_app(app, host = args.host, port = args.port)
	except OSError as err:
		print(f'Error with host/port - {err}')