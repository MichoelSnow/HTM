# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 10:38:29 2017

@author: msnow1
"""

import pandas as pd
from matplotlib.dates import date2num, DateFormatter
import numpy as np
import datetime as dt


def HTMprep(DataFl,timeNm,VarNm):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

def HTMprep2(DataFl):
    cols = DataFl.columns
    var_dict = {cols[0]:["datetime"," "]}
    for i in cols[1:]:
        var_dict[i] = ["float"," "]
    line = pd.DataFrame(var_dict,index=[0,1])
#    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "],VarNm2:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

# %%

appt = pd.read_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_D_2007_2015.csv',
                   na_values="")
appt.APPOINTMENTDATETIME = pd.to_datetime(appt.APPOINTMENTDATETIME, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')

steps = 3
appt.rename(inplace = True, columns = {"APPOINTMENTDATETIME":"timestamp","SHOW":"Ct"})
cols = appt.columns
var_dict = dict()
for i in cols[2:]:
    appt[i] = appt[i].shift(-1*steps,axis=0)
appt = appt.fillna(0)    
appt_htm = HTMprep2(appt)


appt_htm.to_csv("E:\\MyDocuments\\GitHub\\HTM\\Tests\\Appts\\appt_htm_%ssteps.csv" % (steps),index=False)


# %%


appt = pd.read_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_D_2007_2015_zip_dept_age_dist.csv',na_values="")
appt.APPOINTMENTDATETIME = pd.to_datetime(appt.APPOINTMENTDATETIME, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')

steps = 1
appt.rename(inplace = True, columns = {"APPOINTMENTDATETIME":"timestamp","SHOW":"Ct"})
cols = appt.columns
var_dict = dict()
for i in cols[2:]:
    appt[i] = appt[i].shift(-1*steps,axis=0)
appt = appt.fillna(0)    
appt_htm = HTMprep2(appt)


appt_htm.to_csv("E:\\MyDocuments\\GitHub\\HTM\\Tests\\Appts\\appt_htm_%ssteps.csv" % (steps),index=False)
