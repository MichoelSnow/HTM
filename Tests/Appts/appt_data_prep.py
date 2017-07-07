# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 09:54:21 2017

@author: msnow1
"""

import pandas as pd
from matplotlib.dates import date2num, DateFormatter
import numpy as np
import datetime as dt


def HTMprep(DataFl,timeNm,VarNm):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

def HTMprep2(DataFl,timeNm,VarNm,VarNm2):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "],VarNm2:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

def DataSplit(DataFl, Variable, Ranges, Names):
    for i in range(len(Ranges)):
        DataFl[Names[i]] = ((DataFl[Variable]>=Ranges[i][0]) & (DataFl[Variable]<=Ranges[i][1])).astype(int) 
    return DataFl


# %%

appt = pd.read_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_raw.csv', 
                   na_values="", 
                   usecols = ['DOB','SEX','MARITALSTATUSID','APPOINTMENTDATETIME','APPTSTATUSID','APPTCREATEDDATE']) 

appt = appt.dropna()
appt_status = (appt.APPTSTATUSID == 1) | (appt.APPTSTATUSID == 14) | (appt.APPTSTATUSID == 4) | (appt.APPTSTATUSID == 13)
appt = appt[appt_status]

appt.APPOINTMENTDATETIME = pd.to_datetime(appt.APPOINTMENTDATETIME, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
two_months = pd.Timestamp(dt.datetime.now()) - pd.DateOffset(months=2)
#appt = appt[appt.APPOINTMENTDATETIME < two_months]
appt = appt[appt.APPOINTMENTDATETIME < '2016-01-01']

appt.APPTCREATEDDATE = pd.to_datetime(appt.APPTCREATEDDATE, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt.DOB = pd.to_datetime(appt.DOB, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')


appt['Ct'] = 1
appt['AGE'] = ((appt.APPOINTMENTDATETIME - appt.DOB).astype('<m8[Y]')).astype(int)
appt['DIST'] = ((appt.APPOINTMENTDATETIME - appt.APPTCREATEDDATE).astype('<m8[D]')).astype(int)
appt['MARRIED'] = (appt.MARITALSTATUSID== 3).astype(int)
appt['SHOW'] = ((appt.APPTSTATUSID == 1) | (appt.APPTSTATUSID == 14)).astype(int)
appt['MALE'] = (appt.SEX== 'M').astype(int)

age_ranges = [[0,54],[0,17],[18,35],[36,54],[55,70],[71,120]]
age_names = ['AGE_0_54','AGE_0_17','AGE_18_35','AGE_36_54','AGE_55_70','AGE_71_120']
appt = DataSplit(appt,'AGE',age_ranges,age_names)
dist_ranges = [[0,30],[31,60],[61,90],[91,120],[120,365]]
dist_names = ['DIST_0_30','DIST_31_60','DIST_61_90','DIST_91_120','DIST_120_365']
appt = DataSplit(appt,'DIST',dist_ranges,dist_names)

appt_nrw = appt.drop(['DOB','SEX','AGE','MARITALSTATUSID','APPTSTATUSID','APPTCREATEDDATE','DIST'],axis=1)
appt_agg = appt_nrw.resample('D',on='APPOINTMENTDATETIME').sum()
appt_agg = appt_agg.div(appt_agg.Ct,axis=0)

#appt_agg['dates'] = [date2num(date) for date in appt_agg.index]
#MainGraph = appt_agg.plot(x='dates',y=['SHOW','AGE_0_54'])
#dateFormatter = DateFormatter('%m/%d/%y')
#MainGraph.xaxis.set_major_formatter(dateFormatter)  

appt_agg_csv = appt_agg[['SHOW','MARRIED','MALE','AGE_0_54','DIST_0_30']]

#appt_agg_csv = appt_agg_csv[appt_agg_csv.index < '2016-01-01']

#appt_agg_csv.to_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_D.csv')

# %%

appt = pd.read_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_raw_2007_2015.csv', 
                   na_values="")

appt = appt.dropna()
appt_status = (appt.APPTSTATUSID == 1) | (appt.APPTSTATUSID == 14) | (appt.APPTSTATUSID == 4) | (appt.APPTSTATUSID == 13)
appt = appt[appt_status]

appt.APPOINTMENTDATETIME = pd.to_datetime(appt.APPOINTMENTDATETIME, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
two_months = pd.Timestamp(dt.datetime.now()) - pd.DateOffset(months=2)
#appt = appt[appt.APPOINTMENTDATETIME < two_months]
appt = appt[appt.APPOINTMENTDATETIME < '2016-01-01']

appt.APPTCREATEDDATE = pd.to_datetime(appt.APPTCREATEDDATE, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt.DOB = pd.to_datetime(appt.DOB, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')


appt['Ct'] = 1
appt['AGE'] = ((appt.APPOINTMENTDATETIME - appt.DOB).astype('<m8[Y]')).astype(int)
appt['DIST'] = ((appt.APPOINTMENTDATETIME - appt.APPTCREATEDDATE).astype('<m8[D]')).astype(int)
appt['MARRIED'] = (appt.MARITALSTATUSID== 3).astype(int)
appt['SHOW'] = ((appt.APPTSTATUSID == 1) | (appt.APPTSTATUSID == 14)).astype(int)
appt['MALE'] = (appt.SEX== 'M').astype(int)

age_ranges = [[0,54],[0,17],[18,35],[36,54],[55,70],[71,120],[55,120]]
age_names = ['AGE_0_54','AGE_0_17','AGE_18_35','AGE_36_54','AGE_55_70','AGE_71_120','AGE_55_120']
appt = DataSplit(appt,'AGE',age_ranges,age_names)
dist_ranges = [[0,30],[31,60],[61,90],[91,120],[120,365]]
dist_names = ['DIST_0_30','DIST_31_60','DIST_61_90','DIST_91_120','DIST_120_365']
appt = DataSplit(appt,'DIST',dist_ranges,dist_names)

appt_nrw = appt.drop(['DOB','SEX','AGE','MARITALSTATUSID','APPTSTATUSID','APPTCREATEDDATE','DIST'],axis=1)
appt_agg = appt_nrw.resample('D',on='APPOINTMENTDATETIME').sum()
appt_agg = appt_agg.div(appt_agg.Ct,axis=0)

appt_agg['dates'] = [date2num(date) for date in appt_agg.index]
MainGraph = appt_agg.plot(x='dates',y=['SHOW','AGE_0_54','AGE_55_120'])
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)  
MainGraph.legend(tuple(['Show up','0 to 54 years old','55 to 120 years old']), loc=1)
MainGraph.set_xlabel('Dates')
MainGraph.set_ylabel('Percent')
#appt_agg_csv = appt_agg[['SHOW','MARRIED','MALE','AGE_0_54','DIST_0_30']]

#appt_agg_csv = appt_agg_csv[appt_agg_csv.index < '2016-01-01']

#appt_agg_csv.to_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_D_2007_2015.csv')

# %%

appt = pd.read_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_raw.csv', 
                   na_values="", nrows = 5*10**6, 
                   usecols = ['DOB','SEX','MARITALSTATUSID','APPOINTMENTDATETIME','APPTSTATUSID','APPTCREATEDDATE']) 
appt.APPOINTMENTDATETIME = pd.to_datetime(appt.APPOINTMENTDATETIME, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt.APPTCREATEDDATE = pd.to_datetime(appt.APPTCREATEDDATE, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt.DOB = pd.to_datetime(appt.DOB, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')

appt = appt.dropna()
#appt = appt[appt.APPOINTMENTDATETIME < '2017-06-05']
two_months = pd.Timestamp(dt.datetime.now()) - pd.DateOffset(months=2)
appt = appt[appt.APPOINTMENTDATETIME < two_months]

#appt['AGE'] = ((appt.APPOINTMENTDATETIME - appt.DOB).dt.days/365).astype(int)
appt['Ct'] = 1
appt['AGE'] = ((appt.APPOINTMENTDATETIME - appt.DOB).astype('<m8[Y]')).astype(int)
appt.MARITALSTATUSID[appt.MARITALSTATUSID==8] = 6
appt['MARRIED'] = (appt.MARITALSTATUSID== 3).astype(int)
appt['SHOW'] = ((appt.APPTSTATUSID == 1) | (appt.APPTSTATUSID == 14)).astype(int)
#appt['NOSHOW'] = (appt.APPTSTATUSID == 4).astype(int)
appt['MALE'] = (appt.SEX== 'M').astype(int)

age_ranges = [[0,17],[18,35],[36,54],[55,70],[71,120]]
age_names = ['AGE_0_17','AGE_18_35','AGE_36_54','AGE_55_70','AGE_71_120']
appt = DataSplit(appt,'AGE',age_ranges,age_names)


#appt['AGE_0_17'] = (appt.AGE<18).astype(int)
#appt['AGE_18_35'] = ((appt.AGE>=18) & (appt.AGE<36)).astype(int)
#appt['AGE_36_55'] = ((appt.AGE>=36) & (appt.AGE<55)).astype(int)
#appt['AGE_56_120'] = ((appt.AGE>=56) & (appt.AGE<120)).astype(int)


appt_nrw = appt.drop(['DOB','SEX','AGE','MARITALSTATUSID','APPTSTATUSID','APPTCREATEDDATE'],axis=1)
appt_agg = appt_nrw.resample('D',on='APPOINTMENTDATETIME').sum()
appt_agg = appt_agg.div(appt_agg.Ct,axis=0)

#appt_agg = appt.resample('D',on='APPOINTMENTDATETIME').agg({'SHOW': np.sum, 'NOSHOW': np.sum,'AGE': np.mean, 'MALE':np.sum, 'Ct':np.sum})
#appt_agg['SHOWPRCNT'] = appt_agg.SHOW/appt_agg.Ct
#appt_agg['MALEPRCNT'] = appt_agg.MALE/appt_agg.Ct
#appt_agg['0_17_PRCNT'] = appt_agg.AGE_0_17/appt_agg.Ct
#appt_agg['18_35_PRCNT'] = appt_agg.AGE_18_35/appt_agg.Ct
#appt_agg['36_55_PRCNT'] = appt_agg.AGE_36_55/appt_agg.Ct
#appt_agg['56_120_PRCNT'] = appt_agg.AGE_56_120/appt_agg.Ct
appt_agg['dates'] = [date2num(date) for date in appt_agg.index]
MainGraph = appt_agg.plot(x='dates',y=['SHOW','AGE_55_70','AGE_71_120','AGE_36_54'])
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)  

appt_agg_csv.to_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_D.csv')





