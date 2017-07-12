# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:37:00 2017

@author: msnow1
"""

import pandas as pd
from matplotlib.dates import date2num, DateFormatter
#import numpy as np
import datetime as dt

def HTMprep2(DataFl):
    cols = DataFl.columns
    var_dict = {cols[0]:["datetime","T"]}
    for i in cols[1:]:
        var_dict[i] = ["float"," "]
    line = pd.DataFrame(var_dict,index=[0,1])
#    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "],VarNm2:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

# %%

pred = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\PredictionCheck\\data\\gymdata.csv', na_values="",skiprows = [1,2]) 
pred['consumption2'] = pred.consumption.shift(-1,axis=0)


pred = pred.fillna(0)    
pred_htm = HTMprep2(pred)
#pred_htm = pred_htm[['consumption2','consumption']]

pred_htm.to_csv("E:\\MyDocuments\\GitHub\\HTM\\Tests\\PredictionCheck\\data\\pred_htm_cheat.csv" ,index=False)
