# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 16:54:59 2018

@author: USER
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 20:40:27 2018

@author: USER
"""

import unittest

import Mole_in_the_hole
import networkx as nx 


class TestCalc(unittest.TestCase):
    
    def setUp(self):
        self.a = Mole_in_the_hole.MoleInTheHole(topo, source, 
                                               destination, sfc)


    def test_mapping(self):
        self.assertGreater(self.a.path_Mapping(),[])

    def test_dest(self):
        self.assertEqual(self.a.check_destination(), True)
        

    def test_vms(self):
        self.assertEqual(self.a.check_sfc(), True)
        
    def test_layeredgraph(self):
        layered_graph, graph = self.a.create_layeredgraph()
        b = graph.number_of_nodes()
        c = layered_graph.number_of_nodes()
        length = len(sfc) + 1
        total_nodes = b * length
        self.assertGreater(c, b)
        self.assertEqual(total_nodes, c)
        
    def test_sfp(self):
        sfp = []
        osne, no_of_nodes = self.a.MITH()

        ke = sorted(sfc.keys())
        for av in ke:
            for ac in sfc[av]:
                az = int(av) * 18
                ax = int(ac) + int(az)
                if ax in osne:
                    sfp.append(ax)

        if sfp[0] == sfp_check1[0]:
            self.assertEqual(sfp, sfp_check1)
        else:
            self.assertEqual(sfp, sfp_check2)

        
topo = 'Ibm.graphml'
destination = 15
sfc = {'1' : ['1','2'], '2' : ['8'], '3' : ['7']}
source = 0
sfp_check1 = [20, 44, 61]
sfp_check2 = [19, 44, 61]



if __name__ == '__main__':
    unittest.main()
