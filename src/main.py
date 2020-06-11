# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:48:55 2019

@author: anael
"""

from argparse import ArgumentParser as argparse_ArgumentParser
import os
from .sbml2lists import sbml2list
from .network2json import network2
from .py2html import html
from .py2html2 import html2
from .nxvisualizer import network
import networkx as nx
import tarfile
import tempfile
import uuid

def build_parser():
    parser = argparse_ArgumentParser(description='Visualizing a network from sbml')
    parser.add_argument('inputtarfolder',
                        help='Input folder with sbml files as in tar format.')
    parser.add_argument('outfile',
                        help='html file.')
    parser.add_argument('--choice',
                        default="2",
                        help='What kind of input do you want ? \n 1/Single HTML file \n 2/Separated HTML files \n 3/View directly in Cytoscape \n 4/Generate a file readable in Cytoscape \n')
    parser.add_argument('--selenzyme_table',
                        default="N",
                        help='Do you want to display the selenzyme information ? Y/N')
    return parser


def run(tarfolder,outfile,choice="2",selenzyme_table="N"):
    tar = tarfile.open(tarfolder) ##read tar file
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        tar.extractall(path=tmpdirname)
        infolder=tmpdirname

        folders=os.listdir(infolder)
        G=nx.DiGraph()
        scores={}
        scores_col={}
        RdfG_o={}
        RdfG_m={}
        RdfG_uncert={}
        Path_flux_value={}
        Length={}
        revers={}

        for f in folders:
            print(f)

            file=os.path.join(infolder,f)
            output=sbml2list(file, selenzyme_table)
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
            RdfG_o[f]=output[21]
            RdfG_m[f]=output[22]
            RdfG_uncert[f]=output[23]
            if flux_value !={}:
                Path_flux_value[f]=list(flux_value.values())[-1]
            Length[f]=len(LR)-1
            revers=output[24]

            G=network2(G,LR,Lreact,Lprod,name,species_smiles,reac_smiles,images,\
                       images2,species_names,species_links,roots,dic_types,\
                       image2big,data_tab, dfG_prime_o,dfG_prime_m, dfG_uncert,\
                       flux_value, rule_id,rule_score, fba_obj_name,revers)

        scores["dfG_prime_o (kJ/mol)"]=RdfG_o
        scores["dfG_prime_m (kJ/mol)"]=RdfG_m
        scores["dfG_uncert (kJ/mol)"]=RdfG_uncert
        scores["flux_value (mmol/gDW/h)"]=Path_flux_value
        scores["length"]=Length


        if choice == "3": #view in Cytoscape
            network(G,name,outfile)

        elif choice =="4": #generate gml file to view in Cytoscape
            path=os.path.join("cytoscape_files",str(name)+".gml")
            nx.write_gml(G,path)

        elif choice =="1": #view in single html
            html2(G,folders,outfile,scores,scores_col)

        elif choice=="2":#view in separated files
            html(G,folders,outfile,scores,scores_col)


        #Create Tar file
        fid = str(uuid.uuid4())
        tFile = tarfile.open(fid+".tar", 'w')

        files = os.listdir("outfile")
        print(files)
        for f in files:
            tFile.add(os.path.join(os.path.abspath("outfile"),f))

        tFile.close()

    tar.close()


def entrypoint(args=sys_argv[1:]):
    parser = build_parser()
    params = parser.parse_args(args)
    run(arg.inputtarfolder,arg.outfile,arg.choice,arg.selenzyme_table)

##
#
#
if __name__ == "__main__":
    entrypoint(sys_argv[1:])
