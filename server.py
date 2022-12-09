import asyncio

from aiohttp.web import Application, RouteTableDef, HTTPInternalServerError
from serv_plugins.storage import pages, isnull
from serv_plugins.binder import Binder

app = Application()
routes = RouteTableDef()
binder = Binder()

@routes.get(pages.link.main)
async def main_page(request):
	some_page = await binder.get_page(pages.page.main)
	if isnull(some_page):
		raise HTTPInternalServerError()
	else:
		return some_page

@routes.post(pages.link.api)
async def api_page(request):
	pass

@routes.get(pages.link.api)
async def api_page_get(request):
	some_page = await binder.get_page(pages.page.api)
	if isnull(some_page):
		raise HTTPInternalServerError()
	else:
		return some_page

@routes.get(pages.link.open_source)
async def get_open_source(request):
	some_page = await binder.get_page(pages.page.open_source)
	if isnull(some_page):
		raise HTTPInternalServerError()
	else:
		return some_page

if __name__ == '__main__':
	app.add_routes(routes)\
	app.run()