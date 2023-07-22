#import AbstractSSE
#from eventsource.listener import Event, EventSourceHandler
#import eventsource.request as request
#import tornado.web
#import tornado.ioloop

import json
from datetime import datetime
from uuid import uuid4

from flask import Flask
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/event/<action>')
def event(action):
    # user_id = uuid4()
    # dateTimeObj = datetime.now()
    # timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    sse.publish(data=action, type="robotdata")
    return {}, 200


#class SSEendpoint(AbstractSSE.AbstractSSE):
#   def __init__(self, port):
#      self.port = port
#     self.observers = []

    #def startServer(self):
     #   application = tornado.web.Application(
      #      [(r"/poll/listen", EventSourceHandler, dict(event_class=Event, keepalive=2))]) # 127.0.0.1
       # application.listen(self.port) #appllication used to avoid to explicitly create HTTPServer
        #tornado.ioloop.IOLoop.instance().start()

    #def subscribe(self, observer):
     #   self.observers.append(observer)

    #def unsubscribe(self, observer):
     #   self.observers.remove(observer)

    #def notify(self, data):
     #   datastr = " ".join(str(x) for x in data)
      #  request.send_string(r"/", datastr) #'urlvonRESTpostInterface??'
