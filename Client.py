from eventsource.client import EventSourceClient, Event
from Observer import ObserverInterface
from Algorithm import Algorithm
from Waypoint import Waypoint
import zope.interface


import sseclient
import urllib3


def open_stream(url, headers):
    """Get a streaming response for the given event feed using urllib3."""
    http = urllib3.PoolManager()
    return http.request('GET', url, preload_content=False, headers=headers)


if __name__ == '__main__':
    url = 'http://127.0.0.1:5000/stream'
    headers = {'Accept': 'text/event-stream'}
    response = open_stream(url, headers)
    client = sseclient.SSEClient(response)
    stream = client.events()

    while True:
        event = next(stream)
        print(f"event: {event.event} \ndata: {event.data}")

# how to run the app from terminal
# docker run --name redis-sse -p 6379:6379 -d redis (to stop container: docker stop <container id> oder <container name>)
# nächstes mal: docker start <container name>
# gunicorn SSEendpoint:app --worker-class gevent --bind 127.0.0.1:5000

#@zope.interface.implementer(ObserverInterface)
#class Clientside:
 #   def __init__(self, url, action, target):
 #       self.c = EventSourceClient(url=url, action=action, target=target, callback=self.callback, retry=3)
 #       self.algorithm = Algorithm(10, 90)
 #       self.waypoints = []

    # callback function which is called for every received event
 #   def callback(self, event):
 #       print("client")
 #       temp = Waypoint(event.data)
 #       self.waypoints = self.waypoints.append(temp)

 #   def processData(self):
 #       self.c.poll()  # opens connection, also invokes handle_stream() (hopefully)
 #       # after receiving every waypoint for one movement: execute algorithm
 #       self.c.end()
 #       self.algorithm.executeAlgorithm(self.waypoints)
