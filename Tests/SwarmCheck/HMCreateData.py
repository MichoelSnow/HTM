# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 13:51:25 2017

@author: msnow1
"""

import pandas as pd
import numpy as np
from matplotlib.dates import date2num, DateFormatter


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

DtRng = pd.date_range(start = '5/1/2016', end = '5/1/2017', freq = 'H')
HrRng = DtRng.hour
#HolRng = FedHol.holidays(FedHol(),start = DtRng[0],end = DtRng[-1] + pd.Timedelta('365 days'))
#WrkDay = np.logical_and(DtRng.weekday < 5,~(pd.DatetimeIndex(DtRng).normalize()).isin(HolRng))
WrkDay = DtRng.weekday < 5
WrkDay = WrkDay.astype(int) *5+1
DayVal = np.sin(HrRng/24.0*np.pi)*WrkDay

#plt.plot(DayVal)

DtDf = pd.DataFrame({'timestamp':DtRng,'Ct':DayVal})
DtDf = DtDf[['timestamp','Ct']]
DtDf['Shift1'] = DtDf.Ct.shift(-1,axis=0)
DtDf['Shift3'] = DtDf.Ct.shift(-3,axis=0)
DtDf['Shift5'] = DtDf.Ct.shift(-5,axis=0)
#DtDf['Shift7'] = DtDf.Ct.shift(-7,axis=0)
DtDf = DtDf.fillna(0)


#DtDf['dates'] = [date2num(date) for date in DtDf.timestamp]
#MainGraph = DtDf.plot(x='dates',y=['Ct','Shift1','Shift3'])
#dateFormatter = DateFormatter('%m/%d/%y')
#MainGraph.xaxis.set_major_formatter(dateFormatter)  
#DtDf = DtDf.drop(['dates'],axis=1)

DtDf_htm = HTMprep2(DtDf)
DtDf_htm.to_csv('E:\MyDocuments\GitHub\HTM\Tests\SwarmCheck\scdata.csv',index = False)

# %%
DtDf_csv = HTMprep(DtDf,'timestamp','Ct')
DtDf_csv.to_csv('E:\MyDocuments\GitHub\HTM\Tests\HomeMade\HMdataNoHol.csv',index = False)

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





