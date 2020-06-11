#!/usr/bin/env python
# coding: utf-8
'''To visualize a SBML file'''
# In[3]:


import libsbml
import os
import sys
sys.path.insert(0, '/home/rpviz/')
from smile2picture import picture,picture2
from smarts2tab import smarts2tab
#import networkx as nx
#import matplotlib.pyplot as plt



# In[4]:
def sbml2list(file,selenzyme_table):
    
    #open the SBML using libsbml
    
    doc = libsbml.readSBML(file)
    name=os.path.basename(file)
    
    
    # In[8]:
    
    
    #return the model from the SBML document using libsbml
    model = doc.model
    
    
    # In[9]:
    
    
    #we will use the groups package to return the retropath pathway
    #that is all the reactions that are associated with the heterologous 
    #pathway
    groups = model.getPlugin('groups')
    
    
    # In[10]:
    
    
    #in the rpFBA script, rp_pathway is the default name
    rp_pathway = groups.getGroup('rp_pathway') 
    
    annotation = rp_pathway.getAnnotation()
    brsynth_annotation = annotation.getChild('RDF').getChild('BRSynth').getChild('brsynth')
    RdfG_o=brsynth_annotation.getChild('dfG_prime_o').getAttrValue('value')
    RdfG_m=brsynth_annotation.getChild('dfG_prime_m').getAttrValue('value')
    RdfG_uncert=brsynth_annotation.getChild('dfG_uncert').getAttrValue('value')
    
    
    # In[63]:
    
    rlist=[]
    LR=[]
    
    dfG_prime_o = {}
    dfG_prime_m = {}
    dfG_uncert = {}
    flux_value={}
    rule_id={}
    rule_score={}
    reac_smiles={}
    fba_obj_name={}
    revers={}
    
    #loop through all the members of the rp_pathway
    for member in rp_pathway.getListOfMembers():
        #fetch the reaction according to the member id
        reaction = model.getReaction(member.getIdRef())
        rlist.append(reaction)
        LR.append(str(reaction)+"_"+str(name)) #name of reaction node : reaction_pathway
        #get the annotation of the reaction
        #includes the MIRIAM annotation and the IBISBA ones
        annotation = reaction.getAnnotation()
        brsynth_annotation = annotation.getChild('RDF').getChild('BRSynth').getChild('brsynth')
        #extract dG_prime_o of the brsynth annotation values
        dfG_prime_o[str(reaction)+"_"+str(name)] = brsynth_annotation.getChild('dfG_prime_o').getAttrValue('value')
        #extract dG_prime_m of the brsynth annotation values
        dfG_prime_m[str(reaction)+"_"+str(name)] = brsynth_annotation.getChild('dfG_prime_m').getAttrValue('value')
        #extract dG_prime_o of the brsynth annotation values
        dfG_uncert[str(reaction)+"_"+str(name)] = brsynth_annotation.getChild('dfG_uncert').getAttrValue('value')
        #extract rule id from reaction
        rule_id[str(reaction)+"_"+str(name)]=brsynth_annotation.getChild('rule_id').getChild(0).toXMLString()
        #extract rule scor from reaction
        rule_score[str(reaction)+"_"+str(name)]=brsynth_annotation.getChild('rule_score').getAttrValue('value')
        #extract fba_RPFBA_obj value
        flux_value[str(reaction)+"_"+str(name)]=brsynth_annotation.getChild('fba_rpFBA_obj').getAttrValue('value')
        smiles = brsynth_annotation.getChild('smiles').getChild(0).toXMLString()
        if smiles!='None'and smiles!='':
            reac_smiles[str(reaction)+"_"+str(name)] = smiles.replace('&gt;&gt;','>>')
        #Extract name of biomass objective
        biom_obj_name=brsynth_annotation.getChild(6).toXMLString()
        biom_obj_name=(biom_obj_name).split(":")[1].split("units")[0]
        fba_obj_name[str(reaction)+"_"+str(name)]=biom_obj_name
        #extract reversibility of the reaction
        revers[str(reaction)+"_"+str(name)]=reaction.getReversible()
    
   
    
    # In[64]:
    
    
    
    Lreact=[]
    Lprod=[]
    
    for reaction in range(len(rlist)):
        Lreact.append([p.species for p in rlist[reaction].reactants]) #get list of reactants id
        Lprod.append([p.species for p in rlist[reaction].products]) #get list of products id
    
    Listprod=[]
    for j in range(len(Lprod)):
        for i in range(len(Lprod[j])):
            Listprod.append(Lprod[j][i])
            

    Listreact=[]
    for j in range(len(Lreact)):
        for i in range(len(Lreact[j])):
            if Lreact[j][i] not in Listprod : #if it's not a intermediary product
                Lreact[j][i]+='_'+str(name) #name of reactant node is molecule_pathway
            
            if Lreact[j][i] in Listreact: #element already exists:
                c=0
                for k in Listreact: 
                    if Lreact[j][i] in k:
                        c+=1
                Lreact[j][i]+='_'+str(c+1)
            Listreact.append(Lreact[j][i])
    
         
    

    Lelem=[]
    for i in Listprod:
        Lelem.append(i)
    for j in Listreact:
        Lelem.append(j)
        

    dic_types={}

    for i in LR:
        dic_types[i]='reaction'
     
    
    mem = []

    for member in rp_pathway.getListOfMembers():
        reac = model.getReaction(member.getIdRef())
        for rea in reac.getListOfReactants(): #get reactants
            mem.append(rea.getSpecies())
            if rea.getSpecies() not in dic_types:
                if rea.getSpecies() not in Lelem:
                    for elem in Lelem:
                        if rea.getSpecies() in elem: #check the new name of the node
                            dic_types[elem]='reactant'
                else:
                    dic_types[rea.getSpecies()]='reactant'
           
        for pro in reac.getListOfProducts(): #get products
            mem.append(pro.getSpecies())
            dic_types[pro.getSpecies()]='product'
            
        

    
    #mem = list(set([i for i in mem if i[0:3]!='MNX']))

    species_links={}
    species_names={}
    species_smiles={}
    #loop through all the members of the rp_pathway
    for member in list(set([i for i in mem])):
        #fetch the species according to the member id
        reaction = model.getSpecies(member)
        spname=reaction.getName()
        if spname:
            if member not in Lelem:
                for elem in Lelem:
                        if member in elem: #check the new name of the node
                            species_names[elem]=spname
            else :
                species_names[member]=spname
        #get the annotation of the species
        #includes the MIRIAM annotation and the IBISBA ones
        annotation = reaction.getAnnotation()
        brsynth_annotation = annotation.getChild('RDF').getChild('BRSynth').getChild('brsynth')
        #extract one of the brsynth annotation values
        smiles = brsynth_annotation.getChild('smiles').getChild(0).toXMLString()
        if smiles:
            if member not in Lelem:
                for elem in Lelem:
                    if member in elem: #check the new name of the node
                        species_smiles[elem] = smiles
            else:
                species_smiles[member] = smiles
        link_annotation=annotation.getChild('RDF').getChild('Description').getChild('is').getChild('Bag')
        for i in range(link_annotation.getNumChildren()):
            str_annot = link_annotation.getChild(i).getAttrValue(0) #Here we get the attribute at location "0". It works since there is only one
            if str_annot.split('/')[-2]=='metanetx.chemical':
                if member not in Lelem:
                    for elem in Lelem:
                        if member in elem: #check the new name of the node
                            species_links[elem] = str_annot
                else:
                    species_links[member]=str_annot #here is the MNX code returned

    # In[64]:

    
    image=picture(species_smiles)
    image2=picture2(reac_smiles)[0]
    image2big=picture2(reac_smiles)[1]
    if selenzyme_table=='Y':
        data_tab=smarts2tab(reac_smiles)
    else :
        data_tab={i:"" for i in reac_smiles}
    
    roots={}

    for i in range(len(Lprod)):
        for j in Lprod[i]:
            if 'TARGET' in j:
                roots[j]="target"

   
    
    roots[LR[-1]]="target_reaction"
      
    return(LR, Lreact, Lprod, name, species_smiles, reac_smiles,image,image2,\
    species_names, species_links,roots,dic_types,image2big,data_tab,\
    dfG_prime_o,dfG_prime_m, dfG_uncert, flux_value, rule_id,rule_score,\
    fba_obj_name,RdfG_o,RdfG_m,RdfG_uncert,revers)
    
    
        
    
