import similaritymeasures as sim
import xml.etree.ElementTree as ET

if __name__ == '__main__':
    origtree = ET.parse('original90.xml')
    for elem in origtree.iter():
        if elem == 'v1':
            pass
    #origcurve =
    #propcurve =
    #print(sim.frechet_dist(propcurve, origcurve))