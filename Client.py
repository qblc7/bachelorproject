
from Observer import ObserverInterface
from Algorithm import Algorithm
from Waypoint import Waypoint
import zope.interface
import math

import sseclient
import urllib3


@zope.interface.implementer(ObserverInterface)
class Clientside:
    def __init__(self):
        self.algorithm90 = Algorithm(0.0175, 1.57)  # 1-90 Grad
        self.algorithm180 = Algorithm(1.57, math.pi)   # 90-180 Grad
        self.algorithm270 = Algorithm(math.pi, 4.712)  # 180-270 Grad
        self.algorithm360 = Algorithm(4.712, 6.266)  # 270-359 Grad
        self.waypoints = []

    # callback function which is called for every received event
    # adds the newly received event (Waypoint) to a list
    def callback(self, newEvent):
        newData = list(map(float, newEvent.split()))
        temp = Waypoint(newData)
        self.waypoints.append(temp)

    # executes the algorithm to generate the BPMN model
    # for testing thresholds the algorithm is executed several times
    def processData(self):
        self.algorithm90.executeAlgorithm(self.waypoints)
        self.algorithm180.executeAlgorithm(self.waypoints)
        self.algorithm270.executeAlgorithm(self.waypoints)
        self.algorithm360.executeAlgorithm(self.waypoints)

def open_stream(url, headers):
    """Get a streaming response for the given event feed using urllib3."""
    http = urllib3.PoolManager()
    return http.request('GET', url, preload_content=False, headers=headers)

# connect to the REST Servers SSE channel and wait for events
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
            observer.callback(event.data)
    observer.processData()
    print("finished")


