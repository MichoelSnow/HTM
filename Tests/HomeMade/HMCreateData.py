# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 13:51:25 2017

@author: msnow1
"""

import pandas as pd
import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar as FedHol
import matplotlib.pyplot as plt


def HTMprep(DataFl,timeNm,VarNm):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

def HTMprep2(DataFl,timeNm,VarNm,VarNm2):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "],VarNm2:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

DtRng = pd.date_range(start = '5/1/2016', end = '5/1/2017', freq = 'H')
HrRng = DtRng.hour
HolRng = FedHol.holidays(FedHol(),start = DtRng[0],end = DtRng[-1] + pd.Timedelta('365 days'))
WrkDay = np.logical_and(DtRng.weekday < 5,~(pd.DatetimeIndex(DtRng).normalize()).isin(HolRng))
WrkDay = WrkDay.astype(int) *5+1
DayVal = np.sin(HrRng/24.0*np.pi)*WrkDay

#plt.plot(DayVal)

DtDf = pd.DataFrame({'timestamp':DtRng,'Ct':DayVal})
DtDf = DtDf[['timestamp','Ct']]

DtDf_csv = HTMprep(DtDf,'timestamp','Ct')
DtDf_csv.to_csv('E:\MyDocuments\GitHub\HTM\Tests\HomeMade\HMdata.csv',index = False)

HolCntDwn = []
HolCt = 0
NxtHol = HolRng[HolCt]
for i in DtDf.timestamp:
    timDif = int((NxtHol - i).days)+1
    if timDif < 0:
        HolCt+=1
        NxtHol = HolRng[HolCt]
        timDif = int((NxtHol - i).days)
    HolCntDwn.append(timDif)



DtDf['NxtHol'] = HolCntDwn
DtDfHol_csv = HTMprep2(DtDf,'timestamp','Ct','NxtHol')
DtDfHol_csv.to_csv('E:\MyDocuments\GitHub\HTM\Tests\HomeMade\HMdata_FedHol.csv',index = False)





