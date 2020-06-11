# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 09:35:28 2019

@author: anael
"""



import os
import sys
sys.path.insert(0, '/home/rpviz/')
from smile2picture import picture,picture2
from smarts2tab import smarts2tab


    
def csv2list2(csvfolder,path,datapath,datainf,selenzyme_table):
    
    
    name=str(path)
    
    LR=[] #List of reactions
    Lreact=[]
    Lprod=[]
    for i in range(len(datapath)):
        if datapath[i][0]==str(path):#if good pathway
            LR.append((datapath[i][1][:-2])+"/"+name)#problème with the last 0
            Lreact.append(list((datapath[i][3]).split(":")))
            Lprod.append(list((datapath[i][4]).split(":")))
        
    # GET NODES INFORMATION

    
    
   
    species_name={}
    species_smiles={}
    reac_smiles={}
    dic_types={}
    rule_score={}
    rule_id={}
    
    for r in LR:
        dic_types[r]="reaction"
        for i in datainf:     
            if i[1]==r.split("/")[0]: #problem with the last 0   
                reac_smiles[r]=i[2]
                rule_score[r]=i[12]
                rule_id[r]=i[10]
#                species_name[reactant]=i[8]
#                species_smiles[reactant]=i[5]
#                
#              
#                species_name[product]=i[8]
#                species_smiles[product]=i[5]
           
                    
                

       
    
    # To individualize each reactant
    Listprod=[]
    for j in range(len(Lprod)):
        for i in range(len(Lprod[j])):
            Listprod.append(Lprod[j][i])
    
   
    
    Listreact=[]
    for j in range(len(Lreact)):
        for i in range(len(Lreact[j])):
            if Lreact[j][i] not in Listprod : #if not an intermediate product
                Lreact[j][i]+='_'+name
            if Lreact[j][i] in Listreact: #element already exists:
                c=0
                for k in Listreact: 
                    if Lreact[j][i] in k:
                        c+=1
                Lreact[j][i]+='_'+str(c+1)
            Listreact.append(Lreact[j][i])
                
    # SET ATTRIBUTES
    
    sp_names={}
    sp_smiles={}    
    for reac in Listreact:
        dic_types[reac]="reactant"
        for key in species_name.keys():
            if key in reac:
                sp_names[reac]=species_name[key]
                sp_smiles[reac]=species_smiles[key]
    
    for prod in Listprod:
        dic_types[prod]="product"
        
    #Attribute target
    roots={}
    
    
#    for i in range(len(Lprod)):
#        for j in Lprod[i]:
#            if 'TARGET' in j:
#                roots[j]="target"
#    roots[LR[-1]]="target_reaction"
    
    image=picture(sp_smiles)
    image2=picture2(reac_smiles)[0]
    image2big=picture2(reac_smiles)[1]
    
    if selenzyme_table=='Y':
            data_tab=smarts2tab(reac_smiles)
    else :
        data_tab={i:"" for i in reac_smiles}
     
        
    # DELETE USELESS REACTION NODES
#    LR2=[]
#    Lreact2=[]
#    Lprod2=[]
#    for i in range(len(LR)) :
#        if Lreact[i]!=[]:
#            LR2.append(LR[i])
#            Lreact2.append(Lreact[i])
#            Lprod2.append(Lprod[i])

    
    #Attributes not available with the csv
    species_links=dfG_prime_o=dfG_prime_m=dfG_uncert=flux_value\
    =fba_obj_name={}
    RdfG_o=RdfG_m=RdfG_uncert=0

    return(LR, Lreact, Lprod, name, sp_smiles, reac_smiles,image,image2,\
    sp_names, species_links,roots,dic_types,image2big,data_tab,\
    dfG_prime_o,dfG_prime_m, dfG_uncert, flux_value, rule_id,rule_score,\
    fba_obj_name,RdfG_o,RdfG_m,RdfG_uncert)
