class Waypoint:
 def __init__(self, coordinates):
     self.coordinates = coordinates  # list with the 12 coordinates (0-5: joint pos, 6-11: tcp pos)
     self.distances = []
     self.status = "ok"
     self.statdiff = None
     self.diffInTCP = None