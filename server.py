import asyncio
import warnings

from aiohttp.web import Application, RouteTableDef, HTTPInternalServerError, run_app, Response
from argparse import ArgumentParser
from sys import platform
from serv_plugins.storage import pages, isnull
from serv_plugins.binder import Binder
from serv_plugins.ip import self_ip

warnings.filterwarnings('ignore')

if platform in ['linux', 'linux2']:
	try:
		import uvloop
	except ImportError:
		warnings.warn('please, install library "uvloop" for linux before fast job')
	else:
		asyncio.set_event_loop(uvloop.EventLoopPolicy())
elif platform in ['win32', 'cygwin', 'msys']:
	try:
		asyncio.set_event_loop(asyncio.WindowsSelectorEventLoopPolicy())
	except:
		pass

app = Application()
routes = RouteTableDef()
binder = Binder()
parser = ArgumentParser(description = 'Project argument')

parser.add_argument('--host', help = 'Host to listen', default = self_ip())
parser.add_argument('--port', help = 'Port for accept connection', default = '9000')

@routes.get(pages.link.main)
async def main_page(request):
	some_page = await binder.get_page(pages.page.main)
	if isnull(some_page):
		raise HTTPInternalServerError()
	else:
		return Response(text = some_page, content_type='text/html')

@routes.post(pages.link.api)
async def api_page(request):
	pass

@routes.get(pages.link.api)
async def api_page_get(request):
	some_page = await binder.get_page(pages.page.api)
	if isnull(some_page):
		raise HTTPInternalServerError()
	else:
		return Response(text = some_page, content_type='text/html')

@routes.get(pages.link.open_source)
async def get_open_source(request):
	some_page = await binder.get_page(pages.page.open_source)
	if isnull(some_page):
		raise HTTPInternalServerError()
	else:
		return Response(text = some_page, content_type='text/html')

if __name__ == '__main__':
	args = parser.parse_args()
	app.add_routes(routes)
	try:
		run_app(app, host = args.host, port = args.port)
	except OSError as err:
		print(f'Error with host/port - {err}')