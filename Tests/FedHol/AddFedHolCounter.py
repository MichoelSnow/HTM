# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:21:27 2017

@author: msnow1
"""

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as FedHol



def HTMprep(DataFl,timeNm,VarNm,VarNm2):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "],VarNm2:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

Fndng = pd.read_csv('E:\MyDocuments\GitHub\HTM\Tests\FedHol\Fndng_2H_Swarm.csv',
                    skiprows =[1,2],index_col = 'timestamp',parse_dates=True,
                    infer_datetime_format=True)
Fndng.Ct = pd.to_numeric(Fndng.Ct)


HolRng = FedHol.holidays(FedHol(),start = Fndng.index[0],end = Fndng.index[-1] + pd.Timedelta('365 days'))


HolCntDwn = []
HolCt = 0
NxtHol = HolRng[HolCt]
for i in Fndng.index:
    timDif = int((NxtHol - i).days)
    if timDif < 0:
        HolCt+=1
        NxtHol = HolRng[HolCt]
        timDif = int((NxtHol - i).days)
    HolCntDwn.append(timDif)
        
Fndng['NxtHol'] = HolCntDwn
Fndng['timestamp'] = Fndng.index
Fndng = Fndng[['timestamp','Ct','NxtHol']]

Fndng_csv = HTMprep(Fndng,'timestamp','Ct','NxtHol')
