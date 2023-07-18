import zope.interface


class ObserverInterface(zope.interface.Interface):
    c = zope.interface.Attribute("Eventsource Client")
    algorithm = zope.interface.Attribute("Algorithm used to process data")
    waypoints = zope.interface.Attribute("used to store data")
    def __init__(url, action, target):
        pass

    def processData():
        pass

    def callback(event):
        pass
