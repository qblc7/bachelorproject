class Waypoint:
 def __init__(self, coordinates):
     self.coordinates = coordinates
     self.differences = []
     self.status = "ok"
     self.statdiff = None
     self.diffInTCP = None