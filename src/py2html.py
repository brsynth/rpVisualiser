# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:02:54 2019

@author: anael
"""

import json
import os
from bs4 import BeautifulSoup
import networkx as nx
import pandas as pd
import sys
sys.path.insert(0, '/home/rpviz/')
from .color_grad import linear_gradient

def html(G,folder,outfile,scores,scores_col):
    
    
    js = nx.readwrite.json_graph.cytoscape_data(G)
    elements=js['elements']
    
    scores["Choose_a_score"]={i:0 for i in folder}
    
        
    ##Append color dictionaries
    
    for score in scores:
        L=[]
        dic=sorted(scores[score].items(), key=lambda x: float(x[1])) #Compare float not str
      
        for e in dic:
            L.append(e[0]) #list of pathways sorted
 
        nb_diff_col=len(set(list(scores[score].values()))) #how many different values for each score
        hex = linear_gradient("#3a46d5","#da3c29",nb_diff_col)["hex"]
        
        col={}
        if L!=[]:
            col[L[0]]=hex[0] #1st path 1st color
            c=0
            for i in range(1,len(L)):
                if scores[score][L[i]]!=scores[score][L[i-1]]: #if same score, same color
                    c+=1
                col[L[i]]=hex[c]
            
            
            scores_col["col_"+score]=col
        
    ##Append elements in a js file for network
   
    with open(os.path.join(os.path.abspath("outfile"),"network_elements.js"),"w") as jsoutfile:
        jsoutfile.write("obj= "+json.dumps(elements)+"\n")
        jsoutfile.write("scores ="+json.dumps(scores)+"\n")
        jsoutfile.write("scores_col ="+json.dumps(scores_col))
        jsoutfile.close()
    
        
    htmlfile= open(os.path.join(os.path.abspath("rpviz"),"new_html","template.html"))
    soup = BeautifulSoup(htmlfile, 'html.parser')   
  
    select_script=soup.find(id="selectbox")

    for i in scores:
        new_tag=soup.new_tag("option")
        new_tag["value"]=i
        new_tag.append(i)
        select_script.append(new_tag)
    
    #Pathway table        
    pathways = [f for f in folder]
    d={'Pathway':pathways}
    df=pd.DataFrame(d)
    df["Select"]=['' for f in folder]
    df["Score"]=[''for f in folder]
    
    html_str=df.to_html(index=False)
    html_str=html_str.replace("&lt;","<").replace("&gt;",">")
                
    table=soup.find(id="table_path")
    table.append(BeautifulSoup(html_str, 'html.parser'))  
      
        
    htmlfile.close()
        
    html = soup.prettify("utf-8")

    with open(os.path.join(os.path.abspath("outfile"),outfile), "wb") as file:
        file.write(html)    
        
