# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:29:59 2019

@author: anael
"""

from __future__ import print_function
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import rdChemReactions
from rdkit.Chem.Draw import ReactionToImage
from lxml import etree
from urllib import parse


def picture2(rsmile):
    """To draw the reaction"""
    image2={}
    image2big={}
    for i in rsmile:
        r = rdChemReactions.ReactionFromSmarts(rsmile[i], useSmiles=True)
        m = ReactionToImage(r,useSVG=True)
        image=m.split("?>\n")[1] 
        root = etree.fromstring(image, parser=etree.XMLParser()) #resizing html
        header=root.attrib
        width=header['width'][:-2]
        header['width']='385px'
        header['height']='100px'
        header['viewbox']='0 0 '+width+' 200'
        imagemod=etree.tostring(root)
        image2[i]=imagemod.decode("utf-8")
        image2big[i]=image
    return(image2,image2big)
 
def picture(smile):
    """To draw the molecule"""
    image={}
    for i in smile:
        mol = Chem.MolFromSmiles(smile[i])
        drawer = rdMolDraw2D.MolDraw2DSVG(400, 200)
        AllChem.Compute2DCoords(mol)
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText().replace("svg:", "")
        impath = 'data:image/svg+xml;charset=utf-8,' + parse.quote(svg, safe="")
        image[i]=impath
    return(image)
