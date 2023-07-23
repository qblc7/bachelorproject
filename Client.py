from Observer import ObserverInterface
from Algorithm import Algorithm
from Waypoint import Waypoint
import zope.interface

import sseclient
import urllib3


@zope.interface.implementer(ObserverInterface)
class Clientside:
    def __init__(self):
        self.algorithm = Algorithm(10, 90)
        self.waypoints = []

    # callback function which is called for every received event
    def callback(self, newEvent):
        newData = map(float, newEvent.split())
        temp = Waypoint(newData)
        self.waypoints.append(temp)

    def processData(self):
        self.algorithm.executeAlgorithm(self.waypoints)


def open_stream(url, headers):
    """Get a streaming response for the given event feed using urllib3."""
    http = urllib3.PoolManager()
    return http.request('GET', url, preload_content=False, headers=headers)


if __name__ == '__main__':
    observer = Clientside()
    streamNotFinished = True
    url = 'http://127.0.0.1:5000/stream'
    headers = {'Accept': 'text/event-stream'}
    response = open_stream(url, headers)
    client = sseclient.SSEClient(response)
    stream = client.events()

    while streamNotFinished:  # while stream is open
        event = next(stream)
        if event.event == "finished":
            streamNotFinished = False
        else:
            # print(f"event: {event.event} \ndata: {event.data}")
            observer.callback(event.data)
    observer.processData()
    print("finished")


