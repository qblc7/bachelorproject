import math

from Algorithm import Algorithm
from Waypoint import Waypoint
import csv

# reads csv-files with recorded robot data and executes the Algorithm
if __name__ == '__main__':
    observer = Algorithm(0.0175, 1.57)  # 1-90 Grad, TCP: 0,015-1,20
    obs180 = Algorithm(1.57, math.pi)   # 90-180 Grad, TCP: 1,20-1,7
    obs270 = Algorithm(math.pi, 4.712)  # 180-270 Grad
    obs360 = Algorithm(4.712, 6.266)  # 270-359 Grad, TCP: 0,015-1,20
    ########
    obs22_5 = Algorithm(0.0175, 0.393)  # 1-22.5 Grad
    obs45 = Algorithm(0.393, math.pi/4)  # 22.5-45 Grad
    obs67_5 = Algorithm(math.pi/4, 1.178)  # 45-67.5 Grad
    obs90 = Algorithm(1.178, 1.57)  # 67.5-90 Grad
    #######
    obs3 = Algorithm(0.0524, 0.349)  # 3-20 Grad
    obs5 = Algorithm(0.087, 0.349)  # 5-20 Grad
    obs7 = Algorithm(0.122, 0.349)  # 7-20 Grad
    obs9 = Algorithm(0.157, 0.349)  # 9-20 Grad
    ####
    obsDiff2 = Algorithm(0.087, 0.122)  # 5-7 Grad

    # reading robot data from csv files
    waypoints = []
    with open("robot_dataKurve_o2.csv") as data:
        reader = csv.reader(data, delimiter=",")
        next(reader, None)  # skip headers
        for row in reader:  # reads every row as string
            for i in range(0, len(row)):
                newData = list(map(float, row[i].split()))
                temp = Waypoint(newData)
                waypoints.append(temp)
    data.close()
    # re-execute algorithm with different thresholds

    #observer.executeAlgorithm(waypoints)
    #obs180.executeAlgorithm(waypoints)
    #obs270.executeAlgorithm(waypoints)
    #obs360.executeAlgorithm(waypoints)
    #####
    #obs22_5.executeAlgorithm(waypoints)
    #obs45.executeAlgorithm(waypoints)
    #obs67_5.executeAlgorithm(waypoints)
    #obs90.executeAlgorithm(waypoints)
    ########
    obs3.executeAlgorithm(waypoints)
    obs5.executeAlgorithm(waypoints)
    obs7.executeAlgorithm(waypoints)
    obs9.executeAlgorithm(waypoints)
    ###
    #obsDiff2.executeAlgorithm(waypoints)
