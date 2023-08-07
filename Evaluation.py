import similaritymeasures as sim
import xml.etree.ElementTree as ET
import numpy as np
from numpy import dtype

if __name__ == '__main__':
    origtree = ET.parse('original.xml')
    test = []
    origcurve = []
    for elem in origtree.iter():
        if elem.tag == 'v1' or elem.tag == 'v2' or elem.tag == 'v3' or elem.tag == 'v4' or elem.tag == 'v5':
            test.append(float(elem.text))
        if elem.tag == 'v6':
            test.append(float(elem.text))
            origcurve.append(test)
            test = []
    proptree = ET.parse('proposed270.xml')
    propcurve = []
    temp = []
    for elem in proptree.iter():
        if elem.tag == 'v1' or elem.tag == 'v2' or elem.tag == 'v3' or elem.tag == 'v4' or elem.tag == 'v5':
            temp.append(float(elem.text))
        if elem.tag == 'v6':
            temp.append(float(elem.text))
            propcurve.append(temp)
            temp = []
    print(sim.frechet_dist(propcurve, origcurve))
