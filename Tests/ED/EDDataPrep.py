# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:52:37 2017

@author: msnow1
"""

import pandas as pd
from matplotlib.dates import date2num, DateFormatter

def HTMprep(DataFl,timeNm,VarNm):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)

def HTMprep2(DataFl,timeNm,VarNm,VarNm2):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "],VarNm2:["float"," "]},index=[0,1])
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


# %% Plotting the Data

ED = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ED_Timestamp_Ct.csv')
ED = ED.iloc[2:,]
ED.Ct = ED.Ct.astype(float)
ED.timestamp = pd.to_datetime(ED.timestamp, format = "%Y-%m-%d %H:%M:%S")
ED['dates'] = [date2num(date) for date in ED['timestamp']]


MainGraph = ED.plot(x = 'dates',y = 'Ct')
dateFormatter = DateFormatter('%m/%d')
MainGraph.xaxis.set_major_formatter(dateFormatter)


# %%

ED = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ERVisitsTriaged.csv', na_values="") 
ED.TRIAGED = pd.to_datetime(ED.TRIAGED, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
ED = ED[pd.notnull(ED.TRIAGED)]
ED = ED[:][ED.TRIAGED <= '2017/06/27']
ED = ED[:][ED.TRIAGED >= '1997/03/15']
ED['Ct'] = 1
ED = ED.set_index('TRIAGED')
ED_H = ED.resample('H').sum()
ED_H = ED_H.fillna(0)


ED_H['timestamp'] = ED_H.index
ED_H_csv = HTMprep(ED_H,'timestamp','Ct')
ED_H_csv = ED_H_csv[['timestamp','Ct']]
ED_H_csv.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ED_Triaged_Ct.csv', index=False)


ED_plt = ED_H[:]
ED_plt['dates'] = [date2num(date) for date in ED_plt.index]
MainGraph = ED_plt.plot(x = 'dates',y = 'Ct')
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)


ED_2H = ED.resample('2H').sum()
ED_2H = ED_2H.fillna(0)

ED_plt = ED_2H[:]
ED_plt['dates'] = [date2num(date) for date in ED_plt.index]
MainGraph = ED_plt.plot(x = 'dates',y = 'Ct')
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)

ED_2H['timestamp'] = ED_2H.index
ED_2H_csv = HTMprep(ED_2H,'timestamp','Ct')
ED_2H_csv = ED_2H_csv[['timestamp','Ct']]
ED_2H_csv.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ED_Triaged_Ct_2H.csv', index=False)


ED_3H = ED.resample('3H').sum()
ED_3H = ED_3H.fillna(0)
ED_3H['timestamp'] = ED_3H.index
ED_3H_csv = HTMprep(ED_3H,'timestamp','Ct')
ED_3H_csv = ED_3H_csv[['timestamp','Ct']]
ED_3H_csv.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ED_Triaged_Ct_3H.csv', index=False)


# %% ED TIMESTAMP WITH WEATHER DATA

ED = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ERVisitsTriaged.csv', na_values="") 
Wthr = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\NycDailyWeather.csv', na_values="") 
Wthr = Wthr[['DATE','TMAX','TMIN']]
Wthr['TAVG'] = Wthr[['TMAX','TMIN']].mean(axis=1)

ED.TRIAGED = pd.to_datetime(ED.TRIAGED, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
Wthr.DATE = pd.to_datetime(Wthr.DATE, format = "%Y%m%d", errors = 'coerce')

ED = ED[pd.notnull(ED.TRIAGED)]
ED = ED[:][ED.TRIAGED <= '2017/06/23']
ED = ED[:][ED.TRIAGED >= '1997/03/15']
ED['Ct'] = 1

Wthr = Wthr[pd.notnull(Wthr.DATE)]
Wthr = Wthr[:][Wthr.DATE <= '2017/06/23']
Wthr = Wthr[:][Wthr.DATE >= '1997/03/15']

ED_3H = ED.resample('3H', on = 'TRIAGED').sum()
Wthr = Wthr.set_index('DATE')
Wthr_3H = Wthr.resample('3H').ffill()

ED_3H['Tmp'] = Wthr_3H.TAVG
