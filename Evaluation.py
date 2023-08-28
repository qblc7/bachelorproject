import similaritymeasures as sim
import xml.etree.ElementTree as ET

# calculates how similar the original and the proposed path are with the Discrete Frechet Distance (DFD)
if __name__ == '__main__':
    # read the original BPMN from xml-file
    origtree = ET.parse('original_o2.xml')
    test = []
    origcurve = []
    # filter the x,y,z values from the waypoints
    for elem in origtree.iter():
        if elem.tag == 'v1' or elem.tag == 'v2':
            test.append(float(elem.text))
        if elem.tag == 'v3':
            test.append(float(elem.text))
            origcurve.append(test)
            test = []
    # read proposed BPMN from xml-file
    proptree = ET.parse('proposed9_o2.xml')
    propcurve = []
    temp = []
    # filter the x,y,z values from the waypoints
    for elem in proptree.iter():
        if elem.tag == 'v1' or elem.tag == 'v2':
            temp.append(float(elem.text))
        if elem.tag == 'v3':
            temp.append(float(elem.text))
            propcurve.append(temp)
            temp = []
    # calculate DFD and print it
    print(sim.frechet_dist(propcurve, origcurve))
