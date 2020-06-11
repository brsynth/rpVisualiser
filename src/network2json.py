# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:23:33 2019

@author: anael
"""

import networkx as nx
import random



def network2(G,LR,Lreact,Lprod,name,sp_smiles,reac_smiles,image,\
            image2,spname,sp_links,roots,dic_types,\
            image2big, data_tab, dfG_prime_o,dfG_prime_m, dfG_uncert,\
            flux_value, rule_id, rule_score, fba_obj_name, revers):

    ###Create the network with networkx
    col="#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    mem=[]
    for i in LR:
        G.add_node(i,pathway="",colour=col) #add reactions nodes
        mem.append(i)

    
    
#LR=['<Reaction RP1>_rp_3_1', '<Reaction targetSink>_rp_3_1']
#Lreact=[['MNXM2__64__MNXC3_rp_3_1', 'MNXM497__64__MNXC3_rp_3_1'], ['TARGET_0000000001__64__MNXC3']]
#Lprod=[['TARGET_0000000001__64__MNXC3', 'MNXM26__64__MNXC3'], []]
    for i in range(len(LR)):
        for j in range(len(Lreact[i])):
            mem.append(Lreact[i][j])
            if Lreact[i][j] not in G.nodes():
                G.add_node(Lreact[i][j],pathway="")
            G.add_edge(Lreact[i][j],LR[i],pathway=name,colour=col) #add reactants nodes
        for k in range(len(Lprod[i])):
            mem.append(Lprod[i][k])
            if Lprod[i][k] not in G.nodes():
                G.add_node(Lprod[i][k],pathway="")
            G.add_edge(LR[i],Lprod[i][k],pathway=name,colour=col) #add products nodes
    
    #Attribute pathway

    P=nx.get_node_attributes(G,name='pathway')
   
    for i in P: #for each node
        if i in mem: #if nodes is concerned
            if type(P[i])==str:
                a={}
                a[name]=True
                P[i]=a
     
            elif type(P[i])==dict :
                a={}
                a.update(P[i])
                a[name]=True
                P[i]=a
            
        nx.set_node_attributes(G,name='pathway',values=P)

    
    #Attribute name
    nx.set_node_attributes(G,name='name', values=spname)
    
    #Attribute category
    nx.set_node_attributes(G,name='category',values=dic_types)

    #Attribute smile
    nx.set_node_attributes(G, name='smiles', values=sp_smiles)
    
    #Attribute smile
    nx.set_node_attributes(G, name='Rsmiles', values=reac_smiles)
    
    #Attribute image
    nx.set_node_attributes(G,name='image', values=image)
    
    #Attribute reaction image
    nx.set_node_attributes(G,name='image2',values=image2)
    nx.set_node_attributes(G,name='image2big',values=image2big)
    
    #Attribute link
    nx.set_node_attributes(G,name="link",values=sp_links)
    
    #Attribute Root
    nx.set_node_attributes(G,name="root", values=roots)
    
    #Attribute reversibility
    nx.set_node_attributes(G,name="reversibility", values=revers)
    
    #Attribute Data tab
    nx.set_node_attributes(G,name="data_tab", values=data_tab)

    nx.set_node_attributes(G,name="dfG_prime_o", values=dfG_prime_o)
    nx.set_node_attributes(G,name="dfG_prime_m", values=dfG_prime_m)
    nx.set_node_attributes(G,name="dfG_uncert", values=dfG_uncert)
    nx.set_node_attributes(G,name="flux_value", values=flux_value)
    nx.set_node_attributes(G,name="rule_id", values=rule_id)
    nx.set_node_attributes(G,name="rule_score", values=rule_score)
    nx.set_node_attributes(G,name="fba_obj_name", values=fba_obj_name)


    return(G)
    
    
    
