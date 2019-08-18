# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 18:02:19 2018

@author: USER
"""

import networkx as nx

sfc = {'1' : ['1','2'], '2' : ['8'], '3' : ['7']}
name = 'Ibm.graphml'

class MoleInTheHole(object):


    def __init__(self, name, source, destination, node_mapping):
        """
         This method is used for initialization
        Args:
            name: link of graphml file or just name o graphml file
            source: Source node in the network
            destination: destination node in the network
            sfc: VNF to substrate node mapping should be a dict mapping node id
                 to vnf types.
        """

        #Parameters
        self.name = name
        self.source = source
        self.destination = destination
        self.node_mapping = node_mapping


    def read_graphs(self):
        """
        This method is used for reading the graph file 
        Returns:
            Networkx Graph, A node dictionary initialized to zero
        """
        topo = self.name
        G = nx.read_graphml(topo)
        
        return G
    
    def check_source(self):
        """
        It check that source is the part of the network or invalid source. 
        if invalid then raise exception
        Return:
            True or false
        """
        G = self.read_graphs()
        source_bool = False
        for a in G.nodes():
            if a == str(self.source):
                source_bool = True
        if source_bool == False:
            raise Exception('Source is not in Network')
        
        return source_bool


    def check_sfc(self):
        """
        It check that nodes for VNF to substrate node mapping are part 
        of the  network. if invalid then raise exception
        Return:
            True or false
        """
        G = self.read_graphs()
        vm_bool = {}
        vms_bool = False
        for a in self.node_mapping:
            for b in self.node_mapping[a]:                
                vm_bool[b] = False
                
        for a in G.nodes():
            for b in sfc:
                for c in self.node_mapping[b]:
                    if a == c:
                        vm_bool [a] = True

        for c in vm_bool:
            if vm_bool[c] == False:
                raise Exception('Vms is not in Network')
            if c == self.source:
                raise Exception('Source is assgined as VM')
            if c == self.destination:
                raise Exception('Destination is assnied as VM')
            else:
                vms_bool = True
            
        return vms_bool


    def check_destination(self):
        """
        It check that destination is the part of the  network. if invalid then 
        raise exception
        Return:
            True or false
        """
        G = self.read_graphs()
        dest_bool = False
        for a in G.nodes():
            if a == str(self.destination):
                dest_bool = True
        if dest_bool == False:
            raise Exception('Destination is not in Network')
        
        return dest_bool



    
    def create_layeredgraph(self):
        
        """
        This method is for creationg layers by using the orignal graph
        Return:
            Layered graph and orignal graph
        """
        G = self.read_graphs()
        G_dash = nx.Graph()
        no_of_layers = len(self.node_mapping) + 1
        no_of_nodes = G.number_of_nodes()
        c = 0
        # Copy original graph no_of_layers times
        for a in range(0 , no_of_layers):
            for b in G.nodes():
                G_dash.add_node(c) 
                c +=1 
            for x,y in G.edges():
                G_dash.add_edge(int(x) + (no_of_nodes * a), int(y) + 
                                (no_of_nodes * a))
        return G_dash, G
    
    def MITH(self):
        """
        This method is used for getting layered raph and implementing Mole in 
        the hole
        Returns:
            Path from Source to destination on layered graph, and no.of nodes 
            from orignal graph
        """
        G_dash, G = self.create_layeredgraph()
        no_of_layers = len(self.node_mapping) + 1
        no_of_nodes = G.number_of_nodes()
        count = 1    #for checking the layer to connect is the 1st one or other 
        sorted_keys = sorted(self.node_mapping.keys())
    
        for av in sorted_keys:
            edge1 = 0
            edge2 = 0
            for ac in self.node_mapping[av]:
                if count > 1:
                    edge1 = int(ac) + (no_of_nodes * (count - 1)) 
                    edge2 = int(ac) + (count * no_of_nodes)
                    G_dash.add_edge(edge1, edge2)
                else:
                    edge1 = int(ac)
                    edge2 = (int(ac)) + (count * no_of_nodes)
                    G_dash.add_edge(edge1, edge2)
    
            count +=1
    
        destination_dash = self.destination + (no_of_nodes * (no_of_layers
                                                              - 1 ))
        osne = nx.shortest_path(G_dash, self.source, destination_dash)
        
        return osne, no_of_nodes
    
    
    def path_Mapping(self):
        """
        This method is used for taking output from MITH and map it to the
        orignal graph
        Returns:
            Path from Source to destination
        """
        self.check_destination()
        self.check_sfc()
        osne, no_of_nodes = self.MITH()
        path = []
        modified_path = []
        for node_id in osne:
            layer, original_node_id = divmod(node_id, no_of_nodes)
            path.append(original_node_id)
        for a, b in zip(path[0::1], path[1::1]):
            if a != b:
                modified_path.append(a)
        modified_path.append(self.destination)
            
        return modified_path
        

if __name__ == "__main__":
    newobject = MoleInTheHole(name, 0, 15, sfc)
    print newobject.path_Mapping()
    
        