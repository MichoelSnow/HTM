# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 09:54:21 2017

@author: msnow1
"""

import pandas as pd
from matplotlib.dates import date2num, DateFormatter
import numpy as np


def HTMprep(DataFl,timeNm,VarNm):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

def HTMprep2(DataFl,timeNm,VarNm,VarNm2):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "],VarNm2:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)


# %%

appt = pd.read_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_raw.csv', 
                   na_values="", nrows = 5*10**6, 
                   usecols = ['DOB','SEX','MARITALSTATUSID','APPOINTMENTDATETIME',
                              'APPTSTATUSID','APPTCREATEDDATE']) 
appt.APPOINTMENTDATETIME = pd.to_datetime(appt.APPOINTMENTDATETIME, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt.APPTCREATEDDATE = pd.to_datetime(appt.APPTCREATEDDATE, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt.DOB = pd.to_datetime(appt.DOB, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')

appt = appt.dropna()
appt['AGE'] = ((appt.APPOINTMENTDATETIME - appt.DOB).dt.days/365).astype(int)
appt.MARITALSTATUSID[appt.MARITALSTATUSID==8] = 6
appt['SHOW'] = ((appt.APPTSTATUSID == 1) | (appt.APPTSTATUSID == 14)).astype(int)
appt['NOSHOW'] = (appt.APPTSTATUSID == 4).astype(int)
appt['MALE'] = (appt.SEX== 'M').astype(int)
appt['Ct'] = 1
appt['AGE_0_17'] = (appt.AGE<18).astype(int)
appt['AGE_18_35'] = ((appt.AGE>=18) & (appt.AGE<36)).astype(int)
appt['AGE_36_55'] = ((appt.AGE>=36) & (appt.AGE<55)).astype(int)
appt['AGE_56_120'] = ((appt.AGE>=56) & (appt.AGE<120)).astype(int)
appt = appt[appt.APPOINTMENTDATETIME < '2017-07-05']

appt_nrw = appt[(appt.SHOW ==1) | (appt.NOSHOW==1)]
appt_nrw.drop(['DOB','SEX','AGE','MARITALSTATUSID','APPTSTATUSID','APPTCREATEDDATE'],axis=1,inplace=True)


appt_agg = appt_nrw.resample('D',on='APPOINTMENTDATETIME').sum()
#appt_agg = appt.resample('D',on='APPOINTMENTDATETIME').agg({'SHOW': np.sum, 'NOSHOW': np.sum,'AGE': np.mean, 'MALE':np.sum, 'Ct':np.sum})
appt_agg['SHOWPRCNT'] = appt_agg.SHOW/appt_agg.Ct
appt_agg['MALEPRCNT'] = appt_agg.MALE/appt_agg.Ct
appt_agg['0_17_PRCNT'] = appt_agg.AGE_0_17/appt_agg.Ct
appt_agg['18_35_PRCNT'] = appt_agg.AGE_18_35/appt_agg.Ct
appt_agg['36_55_PRCNT'] = appt_agg.AGE_36_55/appt_agg.Ct
appt_agg['56_120_PRCNT'] = appt_agg.AGE_56_120/appt_agg.Ct
appt_agg['dates'] = [date2num(date) for date in appt_agg.index]
MainGraph = appt_agg.plot(x = 'dates',y = ['SHOWPRCNT', 'MALEPRCNT','0_17_PRCNT',
                                           '18_35_PRCNT','36_55_PRCNT','56_120_PRCNT'])
MainGraph = appt_agg.plot(x = 'dates',y = ['SHOWPRCNT', '56_120_PRCNT'])    
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)    


