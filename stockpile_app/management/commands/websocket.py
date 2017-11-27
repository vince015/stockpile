from tornado import (websocket,
                     httpserver,
                     ioloop,
                     web)

from django.core.management.base import BaseCommand
from stockpile_app.websocket.server import WSHandler

class Command(BaseCommand):

    def handle(self, *args, **options):
        app = web.Application([
            (r'/ws', WSHandler),
        ])

        http_server = httpserver.HTTPServer(app)
        http_server.listen(8888)

        myIP = socket.gethostbyname('localhost')
        print('*** Websocket Server Started at {0} ***'.format(myIP))

        ioloop.IOLoop.instance().start()
