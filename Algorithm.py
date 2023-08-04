from Waypoint import Waypoint
import math
import xml.etree.ElementTree as ET


class Algorithm:
    def __init__(self, minA, maxA):
        # thresholds: for joints in radian (joint angles are received in rad), for TCP in meter
        # Grad = rad*(180/pi)
        self.minAngle = minA
        self.maxAngle = maxA
        self.minTCP = abs(2 * 0.85 * math.sin((minA*180/math.pi) / 2))
        self.maxTCP = abs(2 * 0.85 * math.sin((maxA*180/math.pi) / 2))
        # list of programmed waypoints
        self.wps = []

    # calculates all joint/tcp distances between two given waypoints
    # parameters: wp: actual Waypoint, wpPrev: Waypoint of previous timestep
    def calculateDistances(self, wp, wpPrev):
        ok = 0
        missing = 0
        redundant = 0
        for i in range(0, 7):
            # if TCP
            if i == 6:
                temp = math.sqrt(pow((wp.coordinates[i]-wpPrev.coordinates[i]), 2) + pow((wp.coordinates[i+1]-wpPrev.coordinates[i+1]), 2) + pow((wp.coordinates[i+2]-wpPrev.coordinates[i+2]), 2))
                self.compare(temp, self.minTCP, self.maxTCP, wp, True)
            else:  # joints
                temp = abs(wp.coordinates[i] - wpPrev.coordinates[i])
                self.compare(temp, self.minAngle, self.maxAngle, wp, False)
            # not all joints will be moved at the same time: count how many distances classify as what
            if wp.status == "ok":
                ok = ok + 1
            elif wp.status == "redundant":
                redundant = redundant + 1
                wp.status = "ok"
            else:
                missing = missing + 1
                wp.status = "ok"
        # classifying the waypoint -> as long as at least one max<distance>min: wp is ok
        if ok > 0:
            wp.status = "ok"
        elif missing > redundant:
            wp.status = "missing"
        else:
            wp.status = "redundant"
        print(wp.status)

    # checks if the calculated distances are inbetween the min and max and classifies the distance
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
            wp.status = "ok"
            wp.distances.append(d)

    # parameter waypoints: list of programmed waypoints
    def generateProposals(self, waypoints):
        # calculate distances for each waypoint except waypoint 0
        for t in range(1, len(waypoints)):
            self.calculateDistances(waypoints[t], waypoints[t - 1])
        # check status for each waypoint
        #  for t in range(1, len(waypoints)):
        t = 1
        while t < len(waypoints):
            if waypoints[t].status == 'missing':  # case: need more wps
                if waypoints[t].diffInTCP == True:
                    print(f'add {waypoints[t].statdiff / self.maxTCP} more waypoints before {t}')
                else:
                    print(f'add {waypoints[t].statdiff / self.maxAngle} more waypoints before {t}')
                t = t+1
            elif waypoints[t].status == "redundant":  # case: too many wps
                s = t
                # recalculate the distance and status if the wp is removed
                # removes wps until status not "redundant" anymore
                while waypoints[s].status == "redundant" and s < len(waypoints)-1:
                    print(f'remove waypoint {s}')
                    self.calculateDistances(waypoints[s + 1], waypoints[s - 1])
                    s = s + 1
                t = s+1
            else:
                t = t+1

    # parameter wp: list of programmed waypoints
    def executeAlgorithm(self, wp):
        self.wps = wp
        print('min='+str(self.minAngle)+' max='+str(self.maxAngle))
        print('minTCP='+str(self.minTCP)+' maxTCP='+str(self.maxTCP))
        self.generateProposals(self.wps)
        self.generateOriginalBPMN(self.wps)
        self.generateProposedBPMN(self.wps)

    # parameter wp: list of programmed waypoints
    def generateOriginalBPMN(self, wp):
        root = ET.Element("description")
        for i in range(0, len(wp)):
            call = ET.SubElement(root, "call", id="a"+str(i), endpoint="move")
            parameters = ET.SubElement(call, "parameters")
            ET.SubElement(parameters, "label").text = "Move to coords"
            ET.SubElement(parameters, "method").text = ":post"
            arguments = ET.SubElement(parameters, "arguments")
            ET.SubElement(arguments, "v1").text = str(wp[i].coordinates[6])
            ET.SubElement(arguments, "v2").text = str(wp[i].coordinates[7])
            ET.SubElement(arguments, "v3").text = str(wp[i].coordinates[8])
            ET.SubElement(arguments, "v4").text = str(wp[i].coordinates[9])
            ET.SubElement(arguments, "v5").text = str(wp[i].coordinates[10])
            ET.SubElement(arguments, "v6").text = str(wp[i].coordinates[11])
            annotations = ET.SubElement(call, "annotations")
            ET.SubElement(annotations, "_generic")
            timing = ET.SubElement(annotations, "_timing")
            ET.SubElement(timing, "_timing_weight")
            ET.SubElement(timing, "_timing_avg")
            ET.SubElement(timing, "explanations")
            shifting = ET.SubElement(annotations, "_shifting")
            ET.SubElement(shifting, "_shifting_type").text = "Duration"
            context = ET.SubElement(annotations, "_context_data_analysis")
            ET.SubElement(context, "probes")
            ET.SubElement(context, "ips")
            report = ET.SubElement(annotations, "report")
            ET.SubElement(report, "url")
            notes = ET.SubElement(annotations, "_notes")
            ET.SubElement(notes, "_notes_general")
            documentation = ET.SubElement(call, "documentation")
            ET.SubElement(documentation, "input")
            ET.SubElement(documentation, "output")
            implementation = ET.SubElement(documentation, "implementation")
            ET.SubElement(implementation, "description")
        origBpmn = ET.ElementTree(root)
        origBpmn.write("original" + str(self.maxAngle) + ".xml")

    # parameter wp: list of programmed waypoints
    def generateProposedBPMN(self, wp):
        root = ET.Element("description")
        a = 0
        for i in range(0, len(wp)):
            if wp[i].status == "redundant":
                pass
            elif wp[i].status == "missing":
                print("max threshold too small")
            else:
                call = ET.SubElement(root, "call", id="a" + str(a), endpoint="move")
                a = a+1
                parameters = ET.SubElement(call, "parameters")
                ET.SubElement(parameters, "label").text = "Move to coords"
                ET.SubElement(parameters, "method").text = ":post"
                arguments = ET.SubElement(parameters, "arguments")
                ET.SubElement(arguments, "v1").text = str(wp[i].coordinates[6])
                ET.SubElement(arguments, "v2").text = str(wp[i].coordinates[7])
                ET.SubElement(arguments, "v3").text = str(wp[i].coordinates[8])
                ET.SubElement(arguments, "v4").text = str(wp[i].coordinates[9])
                ET.SubElement(arguments, "v5").text = str(wp[i].coordinates[10])
                ET.SubElement(arguments, "v6").text = str(wp[i].coordinates[11])
                annotations = ET.SubElement(call, "annotations")
                ET.SubElement(annotations, "_generic")
                timing = ET.SubElement(annotations, "_timing")
                ET.SubElement(timing, "_timing_weight")
                ET.SubElement(timing, "_timing_avg")
                ET.SubElement(timing, "explanations")
                shifting = ET.SubElement(annotations, "_shifting")
                ET.SubElement(shifting, "_shifting_type").text = "Duration"
                context = ET.SubElement(annotations, "_context_data_analysis")
                ET.SubElement(context, "probes")
                ET.SubElement(context, "ips")
                report = ET.SubElement(annotations, "report")
                ET.SubElement(report, "url")
                notes = ET.SubElement(annotations, "_notes")
                ET.SubElement(notes, "_notes_general")
                documentation = ET.SubElement(call, "documentation")
                ET.SubElement(documentation, "input")
                ET.SubElement(documentation, "output")
                implementation = ET.SubElement(documentation, "implementation")
                ET.SubElement(implementation, "description")
        propBpmn = ET.ElementTree(root)
        propBpmn.write("proposed" + str(self.maxAngle) + ".xml")
