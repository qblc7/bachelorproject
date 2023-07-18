from eventsource.client import EventSourceClient, Event
from Observer import ObserverInterface
from Algorithm import Algorithm
from Waypoint import Waypoint
import zope.interface


@zope.interface.implementer(ObserverInterface)
class Clientside:
    def __init__(self, url, action, target):
        self.c = EventSourceClient(url=url, action=action, target=target, callback=self.callback, retry=3)
        self.algorithm = Algorithm(10, 90)
        self.waypoints = []

    # callback function which is called for every received event
    def callback(self, event):
        print("client")
        temp = Waypoint(event.data)
        self.waypoints = self.waypoints.append(temp)

    def processData(self):
        self.c.poll()  # opens connection, also invokes handle_stream() (hopefully)
        # after receiving every waypoint for one movement: execute algorithm
        self.c.end()
        self.algorithm.executeAlgorithm(self.waypoints)
