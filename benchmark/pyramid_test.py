from pyramid.view import view_config
from pyramid.config import Configurator

@view_config(route_name='json', renderer='json')
def json(request):
    return {'message': 'Hello, World!'}

config = Configurator()

config.add_route('json', '/json')

config.scan()
app = config.make_wsgi_app()
