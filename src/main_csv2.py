# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:32:52 2019

@author: anael
"""


import argparse
import os
import csv
import sys
sys.path.insert(0, '/home/rpviz/')
from csv2list_ind import csv2list2
from network2json import network2
from py2html2 import html2
from nxvisualizer import network
import networkx as nx


def arguments():
    parser = argparse.ArgumentParser(description='Visualizing a network from RetroPath')
    parser.add_argument('infolder', 
                        help='Input folder with csv, json and outpath.')
    parser.add_argument('outfile',
                        help='html file.')
    parser.add_argument('--choice',
                        default="1",
                        help='What kind of input do you want ? \n 1/Single HTML file \n 2/Separated HTML files \n 3/View directly in Cytoscape \n 4/Generate a file readable in Cytoscape \n')
    parser.add_argument('--selenzyme_table',
                        default="N",
                        help='Do you want to display the selenzyme information ? Y/N')

   
    return parser
    

def run(csvfolder,outfile,choice,selenzyme_table):
    
    
    # READ CSV FILE WITH PATHWAYS (out_path)

    csvfilepath=os.path.join(csvfolder,"pathfile","out_paths.csv")
    datapath=[]
    with open(csvfilepath, 'r') as csvFile:
        reader = csv.reader(csvFile)       
        for row in reader:
            datapath.append(row)
    csvFile.close()
    nbpath=int(datapath[-1][0])
   
        
    # READ CSV FILE WITH INFO    (solution)
    
    csvfileinf=list(filter(lambda x: '.csv' in x, os.listdir(csvfolder)))[0]
    datainf=[]
    with open(os.path.join(csvfolder,csvfileinf), 'r') as csvFile:
        reader = csv.reader(csvFile)   
        for row in reader:
            datainf.append(row)
    csvFile.close()
  
  
    G=nx.DiGraph()
    scores={}
    scores_col={}
    RdfG_o={}
    RdfG_m={}
    RdfG_uncert={}
    Path_flux_value={}
    Length={}
   
    for path in range(1,nbpath+1): #for each pathway
        print(path)
        output=csv2list2(csvfolder,path, datapath, datainf,selenzyme_table)
        
        LR=output[0]
        Lreact=output[1]
        Lprod=output[2]
        name=output[3]
        species_smiles=output[4]
        reac_smiles=output[5]
        images=output[6]
        images2=output[7]
        species_names=output[8]
        species_links=output[9]
        roots=output[10]
        dic_types=output[11]
        image2big=output[12]
        data_tab=output[13]
        dfG_prime_o=output[14]
        dfG_prime_m=output[15]
        dfG_uncert=output[16]
        flux_value=output[17]
        rule_id=output[18]
        rule_score=output[19]
        fba_obj_name=output[20]
        RdfG_o[path]=output[21]
        RdfG_m[path]=output[22]
        RdfG_uncert[path]=output[23]
        if flux_value!={}:
            Path_flux_value[path]=list(flux_value.values())[-1]
        else :
            Path_flux_value={}
            
        Length[path]=len(LR)-1
        
        G=network2(G,LR,Lreact,Lprod,name,species_smiles,reac_smiles,images,\
                   images2,species_names,species_links,roots,dic_types,\
                   image2big,data_tab, dfG_prime_o,dfG_prime_m, dfG_uncert,\
                   flux_value, rule_id,rule_score, fba_obj_name)
        
        scores["dfG_prime_o (kJ/mol)"]=RdfG_o
        scores["dfG_prime_m (kJ/mol)"]=RdfG_m
        scores["dfG_uncert (kJ/mol)"]=RdfG_uncert
        scores["flux_value (mmol/gDW/h)"]=Path_flux_value
        scores["length"]=Length
  
    if choice == "3": #view in cytoscape
        network(G,name,outfile)
        
    elif choice =="4":
        path=os.path.join("cytoscape_files",str(name)+".gml")
        nx.write_gml(G,path)
            
    if choice =="1": #view in single html
        html2(G,range(1,nbpath+1),outfile,scores,scores_col)

  
#    elif choice=="2":
#        html(json_elements,outfile)
#        


if __name__ == '__main__':
    parser = arguments()
    arg = parser.parse_args()
    run(arg.infolder,arg.outfile,arg.choice,arg.selenzyme_table)
