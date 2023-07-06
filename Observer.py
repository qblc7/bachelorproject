import zope.interface


class Observer(zope.interface.Interface):
    def __init__(self):
        pass

    def processData(self):
        pass
