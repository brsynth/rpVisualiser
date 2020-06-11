# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:21:48 2019

@author: anael
"""
#Usefull
import inspect
#inspect.getargspec(function)

import networkx as nx
from IPython.display import Image
import requests
import json
import pandas as pd

# Library for util
import sys
sys.path.insert(0, '/home/rpviz/')
from py2cytoscape.data.cynetwork import CyNetwork
from py2cytoscape.data.cyrest_client import CyRestClient
from py2cytoscape.data.style import StyleUtil


def network(G,name,outfile):
     #Connect with cytoscape
    cy = CyRestClient()
    
    # Reset
    #cy.session.delete()
    
    #To create the network in cytoscape
    network = cy.network.create_from_networkx(G, name=name, collection=str(outfile))
    #print('New network created with py2cytoscape.  Its SUID is ' + str(network.get_id()))
    
    #To get the SUID of all the components of the network
    all_suid = cy.network.get_all()
    net1 = cy.network.create(all_suid[0])
    #print(net1.get_first_view())
    
    #Styles
    cy.layout.apply(name='hierarchical', network=network)
    
    # Get all existing Visual Styles
    styles = cy.style.get_all()
    #print(json.dumps(styles, indent=4))
    
    
    # Get a reference to the existing style
    default_style = cy.style.create('default')
    #print(default_style.get_name())
    
    # Get all available Visual Properties
    #print(len(cy.style.vps.get_all()))
    node_vps=cy.style.vps.get_node_visual_props()
    edge_vps = cy.style.vps.get_edge_visual_props()
    network_vps=cy.style.vps.get_network_visual_props()
    #print(pd.Series(edge_vps).head())
    #print(pd.Series(node_vps).head())
    
    
    # Create a new style
    style1 = cy.style.create("My_style")
    #print(style1.get_name())
    
    
    new_defaults = {
        # Node defaults
        'NODE_FILL_COLOR': '#00ddee',
        'NODE_SIZE': 20,
        'NODE_BORDER_WIDTH': 0,
        'NODE_LABEL_COLOR': 'black',
        
        # Edge defaults
        'EDGE_WIDTH': 3,
        'EDGE_STROKE_UNSELECTED_PAINT': '#aaaaaa',
        'EDGE_LINE_TYPE': 'LONG_DASH',
        'EDGE_TARGET_ARROW_SHAPE' : 'DELTA',
        
        # Network defaults
        'NETWORK_BACKGROUND_PAINT': 'white',
    }
    
    style1.update_defaults(new_defaults)
    #Apply style
    cy.style.apply(style1, network)
    
    # Passthrough mapping to get node labels
    style1.create_passthrough_mapping(column='name', col_type='String', vp='NODE_LABEL')
    
    # Discrete mapping for node colours:
    cat = {
        'reactant': '#4D833C',
        'product': '#C04E5D'
    }
    style1.create_discrete_mapping(column='category', 
                                   col_type='String', 
                                   vp='NODE_FILL_COLOR', 
                                   mappings=cat)
    
    # Discrete mapping for node shape:
    reac = {
        'reactions': 'RECTANGLE'
    }
    style1.create_discrete_mapping(column='category', 
                                   col_type='String', 
                                   vp='NODE_SHAPE', 
                                   mappings=reac)
    
