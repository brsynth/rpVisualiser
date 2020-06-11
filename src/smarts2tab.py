# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 09:23:37 2019

@author: anael
"""

import requests
import json
import pandas as pd

#smarts={"smarts":"O=O.[H]Oc1c([H])c([H])c([H])c([H])c1O[H]>>[H+].[H+].[H]OC(=O)C([H])=C([H])C([H])=C([H])C(=O)O[H]"}

def smarts2tab(smarts):
    tab_data={}
    for i in smarts :
  
        api = "http://selenzyme.synbiochem.co.uk/REST/Query"
        data={"smarts": smarts[i]}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        
        r=requests.post(url=api,data=json.dumps(data),headers=headers)
        response=r.json()['data']
        if response!=None :
          
            response=json.loads(response)
            
        
            df=pd.DataFrame.from_dict(response) #create a data frame from the dict
            df=df.loc[['1','2','3','4','5']]
            df=df.iloc[:,:5]
            data=df.to_dict()
  
            #data=json.dumps(data)
            
            tab_data[i]=data

    return(tab_data)
