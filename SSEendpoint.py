#import AbstractSSE
#from eventsource.listener import Event, EventSourceHandler
#import eventsource.request as request
#import tornado.web
#import tornado.ioloop


from flask import Flask
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/event/<action>')
def event(action):
    if action == "finished":
        sse.publish(data="finished", type="finished")
        return {}, 200
    else:
        sse.publish(data=action, type="robotdata")
        return {}, 200

# how to run the app from terminal:
# docker run --name redis-sse -p 6379:6379 -d redis (to stop container: docker stop <container id> oder <container name>)
# nächstes mal: docker start <container name>
# gunicorn SSEendpoint:app --worker-class gevent --bind 127.0.0.1:5000

# how to run docker robot simulation:
# docker run --rm -it universalrobots/ursim_e-series



#class SSEendpoint(AbstractSSE.AbstractSSE):
#   def __init__(self, port):
#      self.port = port
#     self.observers = []

    #def subscribe(self, observer):
     #   self.observers.append(observer)

    #def unsubscribe(self, observer):
     #   self.observers.remove(observer)

    #def notify(self, data):
     #   datastr = " ".join(str(x) for x in data)
      #  request.send_string(r"/", datastr) #'urlvonRESTpostInterface??'
