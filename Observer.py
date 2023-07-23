import zope.interface


class ObserverInterface(zope.interface.Interface):
    algorithm = zope.interface.Attribute("Algorithm used to process data")
    waypoints = zope.interface.Attribute("used to store data")
    def __init__():
        pass

    def processData():
        pass

    def callback(event):
        pass
