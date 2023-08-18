import math

from Algorithm import Algorithm
from Waypoint import Waypoint
import csv

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
    #w1 = Waypoint([5.027843475341797, -1.1360243123820801, 1.1939199606524866, 4.564928217525146, -1.458081070576803, -5.593887154256002, -0.3734197744316392, 0.6107684546389476, 0.24600848986167656, -3.054511620612435, 0.5680279116028478, 0.21694808100773125])
    #w2 = Waypoint([4.68212366104126, -1.5450957168689747, 1.1066983381854456, 4.567531271571777, -1.4581168333636683, -5.593851153050558, -0.14703496138521968, 0.6140507325035817, 0.5677087376759478, -2.445332865923505, 0.872554837559796, 0.38664908692214495])
    #w3 = Waypoint([3.876007556915283, -1.0653831523707886, 1.1560629049884241, 4.965081679611959, -1.4580567518817347, -5.594066683446066, 0.3297097982510891, 0.5206141528506351, 0.1926164168716521, 2.0076683382693616, -1.9559187356706016, -0.18888256632020975])
    #w1_2 = Waypoint([5.027879238128662, -1.1917103093913575, 1.193463150654928, 4.56526438772168, -1.4581406752215784, -5.593887154256002, -0.371671520422324, 0.6053484618526378, 0.28484870104534654, -3.0043479723967805, 0.5538672258519968, 0.25439586572031975])
    #w1_1 = Waypoint([5.027867317199707, -1.1360003513148804, 1.1938827673541468, 4.564963980312012, -1.458081070576803, -5.593875233327047, -0.3734353220182811, 0.6107626657498217, 0.24600654986218745, -3.054537500399846, 0.5680160699710903, 0.21693359007779284])
    #wp = [w1, w1_1, w1_2, w2, w3]
    #observer.executeAlgorithm(wp)

    # reading robot data from csv files to re-execute algorithm with different thresholds
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
    #obs3.executeAlgorithm(waypoints)
    #obs5.executeAlgorithm(waypoints)
    #obs7.executeAlgorithm(waypoints)
    #obs9.executeAlgorithm(waypoints)
    ###
    obsDiff2.executeAlgorithm(waypoints)
