from Waypoint import *
import math
import xml.etree.ElementTree as ET


class Algorithm:
    def __init__(self, minA, maxA):
        # thresholds: for joints in angle, for TCP in meter
        self.minAngle = minA
        self.maxAngle = maxA
        self.minTCP = 2 * 0.85 * math.sin(minA / 2)
        self.maxTCP = 2 * 0.85 * math.sin(maxA / 2)
        # list of programmed waypoints
        self.wps = []

    # calculates all joint/tcp distances between two given waypoints
    def calculateDistances(self, wp, wpPrev):
        for i in range(0, 7):
            # if TCP
            if i == 6:
                temp = math.sqrt(pow((wp[i]-wpPrev[i]), 2) + pow((wp[i+1]-wpPrev[i+1]), 2) + pow((wp[i+2]-wpPrev[i+2]), 2))
                self.compare(temp, self.minTCP, self.maxTCP, wp, True)
            else:  # joints
                temp = wp.coordinates[i] - wpPrev.coordinates[i]
                self.compare(temp, self.minAngle, self.maxAngle, wp, False)

    # checks if the calculated distances are inbetween the min and max and classifies the waypoint
    def compare(self, d, min, max, wp, tcp):
        if d < min:
            wp.distances.append(d)
            # check if status was changed already
            if wp.status == "ok":
                wp.status = "redundant"
                wp.statdiff = d
                if tcp:
                    wp.diffInTCP = True
        elif d > max:
            wp.distances.append(d)
            wp.status = "missing"
            wp.statdiff = d
            if tcp:
                wp.diffInTCP = True
        else:  # OK
            wp.distances.append(d)

    def generateProposals(self, waypoints):
        # calculate distances for each waypoint except waypoint 0
        for t in range(1, len(waypoints)):
            self.calculateDistances(waypoints[t], waypoints[t - 1])
        # check status for each waypoint
        for t in range(1, len(waypoints)):
            if waypoints[t].status == 'missing':  # case: need more wps
                if waypoints[t].diffInTCP == True:
                    print("add " + waypoints[t].statdiff / self.maxTCP + " more waypoints before t")
                else:
                    print("add " + waypoints[t].statdiff / self.maxAngle + " more waypoints before t")
            elif waypoints[t].status == "redundant":  # case: too many wps
                s = t
                # recalculate the distance and status if the wp is removed
                # removes wps until status not "redundant" anymore
                while waypoints[s].status == "redundant":
                    print("remove waypoint" + s)
                    self.calculateDistances(waypoints[s + 1], waypoints[s - 1])
                    s = s + 1
            else:
                pass

    # parameter wp: list of programmed waypoints
    def executeAlgorithm(self, wp):
        self.wps = wp
        self.generateProposals(self.wps)
        self.generateOriginalBPMN(self.wps)
        self.generateProposedBPMN(self.wps)

    def generateOriginalBPMN(self, wp):
        root = ET.Element('description xmlns="http://cpee.org/ns/description/1.0"/')
        for i in range(0, len(wp)):
            ET.SubElement(root, "manipulate", id=str(i), label="post").text = str(wp[i])  # -----?
        origBpmn = ET.ElementTree(root)
        origBpmn.write("original.xml")

    def generateProposedBPMN(self, wp):
        root = ET.Element('description xmlns="http://cpee.org/ns/description/1.0"/')
        for i in range(0, len(wp)):
            if wp[i].status == "redundant":
                pass
            elif wp[i].status == "missing":
                print("max threshold too small")
            else:
                ET.SubElement(root, "manipulate", id=str(i), label="post").text = str(wp[i])  # -----?
        propBpmn = ET.ElementTree(root)
        propBpmn.write("proposed.xml")
