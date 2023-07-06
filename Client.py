from eventsource.client import EventSourceClient, Event

import Observer
from Algorithm import Algorithm
from Waypoint import Waypoint


class Client(Observer.Observer):
    def __init__(self, url, action, target):
        super().__init__()
        self.Client = EventSourceClient(url=url, action=action, target=target, callback=self.callback, retry=3)
        self.algorithm = Algorithm(10, 90)
        self.waypoints = []

    # callback function which is called for every received event
    def callback(self, event):
        temp = Waypoint(event.data)
        self.waypoints = self.waypoints.append(temp)

    def processData(self):
        self.Client.poll()  # also invokes handle_stream() (hopefully)
        # after receiving every waypoint for one movement: execute algorithm
        self.algorithm.executeAlgorithm(self.waypoints)
        self.Client.end()
