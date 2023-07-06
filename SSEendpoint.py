import AbstractSSE
from eventsource.listener import JSONEvent, EventSourceHandler
import tornado.web
import tornado.ioloop


class SSEendpoint(AbstractSSE.AbstractSSE):
    def __init__(self, port):
        self.port = port

    def startServer(self):
        application = tornado.web.Application(
            [("r / (.*) / (.*)", EventSourceHandler, dict(event_class=JSONEvent, keepalive=2))])
        application.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()
