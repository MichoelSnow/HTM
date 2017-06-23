# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:52:37 2017

@author: msnow1
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.dates import date2num, DateFormatter

def HTMprep(DataFl,timeNm,VarNm):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

# %% ED Timestamp data

ED = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ERVisitsTimeStamp.csv', na_values="") 
ED.CREATEDATETIME = pd.to_datetime(ED.CREATEDATETIME, format = "%d-%b-%y %I.%M.%S.%f %p")
ED['Ct'] = 1
ED = ED.set_index('CREATEDATETIME')
ED_H = ED.resample('H').sum()
ED_H = ED_H.fillna(0)
ED_H.plot()

ED_H['timestamp'] = ED_H.index

ED_H_csv = HTMprep(ED_H,'timestamp','Ct')
ED_H_csv = ED_H_csv[['timestamp','Ct']]

ED_H_csv.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ED_Timestamp_Ct.csv', index=False)


# %%

ED = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ERVisitsDate.csv', na_values="") 
ED.TRIAGED = pd.to_datetime(ED.TRIAGED, format = "%d-%b-%y")
ED['Ct'] = 1
ED = ED.set_index('TRIAGED')
ED_D = ED.resample('D').sum()
ED_D.plot()
ED_D = ED_D[:][ED_D.index <= '2017/06/01']

ED_D['timestamp'] = ED_D.index
ED_D_csv = HTMprep(ED_D,'timestamp','Ct')
ED_D_csv = ED_D_csv[['timestamp','Ct']]

ED_D_csv.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ED_Date_Ct.csv', index=False)
