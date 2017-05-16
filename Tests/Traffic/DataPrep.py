# -*- coding: utf-8 -*-
"""
Created on Thu May 11 07:57:46 2017

@author: msnow1
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.dates import date2num, DateFormatter


def lookup(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date:pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)
# %%
#TrffcAp = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\april2017.csv', na_values="") 
#TrffcMr = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\march2017.csv', na_values="") 
#TrffcFb = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\february2017.csv', na_values="") 
#TrffcJa = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\january2017.csv', na_values="") 
TrffcDe = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\december2016.csv', na_values="") 
TrffcNo = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\november2016.csv', na_values="") 
TrffcOc = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\october2016.csv', na_values="") 
TrffcSe = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\september2016.csv', na_values="") 
TrffcAu = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\august2016.csv', na_values="") 
TrffcJl = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\july2016.csv', na_values="") 
TrffcJn = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\june2016.csv', na_values="") 
TrffcMy = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\may2016.csv', na_values="") 
TrffcAp = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\april2016.csv', na_values="") 
TrffcMr = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\march2016.csv', na_values="") 
TrffcFb = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\february2016.csv', na_values="") 
TrffcJa = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\january2016.csv', na_values="") 

TrffcCat = pd.concat([TrffcJa,TrffcFb,TrffcMr,TrffcAp,TrffcMy,TrffcJn,TrffcJl,TrffcAu,TrffcSe,TrffcOc,TrffcNo,TrffcDe])
TrffcCat.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\2016.csv', index=True)
# %%
TrffcById = TrffcCat[:][TrffcCat['Id']==MxVl[0][1]]
TrffcById = TrffcById.drop_duplicates(subset = 'DataAsOf')
TrffcById['DataAsOf'] = lookup(TrffcById['DataAsOf'])
TrffcById = TrffcById.sort_values('DataAsOf')
TrffcById = TrffcById.set_index('DataAsOf')


TrffcById['dates'] = [date2num(date) for date in TrffcById.index]

MainGraph = TrffcById.plot(x = 'dates', y='Speed')
dateFormatter = DateFormatter('%m/%d')
MainGraph.xaxis.set_major_formatter(dateFormatter)

TrffcById_20T = TrffcById.resample('20T').mean()
TrffcById_20T_v2 = TrffcById_20T.dropna(axis = 0, how=  'all')

TrffcById_3H = TrffcById.resample('4H').mean()
MainGraph = TrffcById_3H.plot(x = 'dates', y='Speed')
dateFormatter = DateFormatter('%m/%d')
MainGraph.xaxis.set_major_formatter(dateFormatter)

MainGraph = TrffcById_20T.plot(x = 'dates', y='Speed')
dateFormatter = DateFormatter('%m/%d')
MainGraph.xaxis.set_major_formatter(dateFormatter)


TrffcById.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\2016_ID184.csv', index=True)
TrffcById_20T_v2.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\2016_ID184_20T.csv', index=True)
# %%

TrffcByIdSml = TrffcById.drop(['Id','TravelTime','Status','linkId','dates'],axis = 1)
TrffcByIdSml = TrffcById['Speed']
TrffcByIdSml.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\2016_Sml.csv', index=True)

TrffcByIdSml.index.names = ['timestamp']

line = pd.DataFrame({'timestamp':["datetime"," "],'Speed':["float"," "]},index=[0,1])
line = line.set_index('timestamp')
TrffcByIdSml_csv = pd.concat([line, TrffcByIdSml])
TrffcByIdSml_csv.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\2016_Sml.csv', index=True)


TrffcById_20T_csv = pd.concat([line, TrffcById_20T_v2])
TrffcById_20T_csv.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Traffic\\2016_Sml_20T.csv', index=True)



# %%
TrffcTmp = pd.concat([TrffcFb,TrffcMr,TrffcAp])
TrffcTmp = TrffcTmp[:][TrffcTmp['Id']==MxVl[4][1]]
TrffcTmp = TrffcTmp.drop_duplicates(subset = 'DataAsOf')
# %%
Trffc['DataAsOf'] = lookup(Trffc['DataAsOf'])
# %%
TrffcIds = sorted(TrffcTmp.Id.unique())
MxVl = []
for i in TrffcIds:
    Trffc1 = TrffcTmp[:][TrffcTmp['Id']==i]
    Trffc1 = Trffc1.drop_duplicates(subset = 'DataAsOf')
#    if len(Trffc1) > MxVl[0]:
    MxVl.append([len(Trffc1),i])
    
MxVl = sorted(MxVl,reverse=True)    
# %%    
# 184, 159, 154, 170    
    
Trffc1 = Trffc[:][Trffc['Id']==3]
Trffc1 = Trffc1.sort_values('DataAsOf')
Trffc1 = Trffc1.set_index('DataAsOf')
Trffc1 = Trffc1.drop_duplicates(subset = 'DataAsOf')
print len(Trffc1)
#FndngOut['dates'] = [date2num(date) for date in FndngOut['timestamp']]





# %%
Fndng = FndngFull[5]
Fndng = pd.to_datetime(Fndng, format = '%Y-%m-%d %H:%M:%S')
Fndng = pd.to_datetime(Fndng, infer_datetime_format=True)



Fndng = FndngFull[[5,9]].copy()
Fndng[5] = lookup(Fndng[5])

Fndng = Fndng.set_index([5])
Fndng['Ct'] = pd.Series([1]*len(Fndng), index=Fndng.index)
Fndng.index.name = 'timestamp'
Fndng = Fndng[:][Fndng.index >= '2016/12/30']

Fndng_H = Fndng.resample('H').sum()
Fndng_H = Fndng_H.fillna(0)
Fndng_H.plot()

Fndng_90T = Fndng.resample('90T').sum()
Fndng_90T = Fndng_90T.fillna(0)
Fndng_90T.plot()

Fndng_2H = Fndng.resample('2H').sum()
Fndng_2H = Fndng_2H.fillna(0)
Fndng_2H.plot()

# create the swarm ready version of the files
SwarmPrepend = pd.DataFrame({'Ct':["float"," "]},index=['datetime',''])
SwarmPrepend.index.name = 'timestamp'


Fndng_H.to_csv('E:\MyDocuments\HTM\Finding\Fndng_H.csv', index=True)
Fndng_H_Swarm = SwarmPrepend.append(Fndng_H)
Fndng_H_Swarm.to_csv('E:\MyDocuments\HTM\Finding\Fndng_H_Swarm.csv', index=True)

Fndng_2H.to_csv('E:\MyDocuments\HTM\Finding\Fndng_2H.csv', index=True)
Fndng_2H_Swarm = SwarmPrepend.append(Fndng_2H)
Fndng_2H_Swarm.to_csv('E:\MyDocuments\HTM\Finding\Fndng_2H_Swarm.csv', index=True)

# %%


FndngOut = pd.read_csv('E:\MyDocuments\HTM\Finding\Fndng_2H_Swarm_out.csv', na_values="") 

FndngOut['timestamp'] = lookup(FndngOut['timestamp'])
FndngOut['dates'] = [date2num(date) for date in FndngOut['timestamp']]

fig = plt.figure(figsize=(8, 6)) 

gs = gridspec.GridSpec(2,1, height_ratios=[3, 1]) 
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1], sharex=ax0)
ax1.set_color_cycle(['m', 'r'])
MainGraph = FndngOut.plot(x = 'dates', y=['Ct','prediction'], ax = ax0)
AnomalyGraph = FndngOut.plot(x = 'dates', y=['anomalyScore','anomaly_likelihood'], ax=ax1)


dateFormatter = DateFormatter('%m/%d')
MainGraph.xaxis.set_major_formatter(dateFormatter)
AnomalyGraph.xaxis.set_major_formatter(dateFormatter)

ax0.set_ylabel('Lab Count')
ax1.set_ylabel('Percent')
ax1.set_xlabel('Dates')

MainGraph.legend(tuple(['actual', 'predicted']), loc=3)
AnomalyGraph.legend(tuple(['anomaly score','anomaly likelihood']), loc=3)


# %%

RC = pd.read_csv('E:\MyDocuments\HTM\Finding\\rec-center-hourly_out.csv', na_values="") 
RC['timestamp'] = lookup(RC['timestamp'])
RC['dates'] = [date2num(date) for date in RC['timestamp']]

fig = plt.figure(figsize=(8, 6)) 

gs = gridspec.GridSpec(2,1, height_ratios=[3, 1]) 
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1], sharex=ax0)
ax1.set_color_cycle(['m', 'r'])
MainGraph = RC.plot(x = 'dates', y=['kw_energy_consumption','prediction'], ax = ax0)
AnomalyGraph = RC.plot(x = 'dates', y=['anomalyScore','anomaly_likelihood'], ax=ax1)

dateFormatter = DateFormatter('%m/%d')
MainGraph.xaxis.set_major_formatter(dateFormatter)
AnomalyGraph.xaxis.set_major_formatter(dateFormatter)

ax0.set_ylabel('Consumption')
ax1.set_ylabel('Percent')
ax1.set_xlabel('Dates')

MainGraph.legend(tuple(['actual', 'predicted']), loc=3)
AnomalyGraph.legend(tuple(['anomaly score','anomaly likelihood']), loc=3)


# %%
RC['timestamp'] = lookup(RC['timestamp'])
RC['timestamp'] = RC['timestamp'].map(lambda t: t.strftime('%j'))
RC['timestamp'] = RC['timestamp'].astype(str)
RC = RC.set_index(['timestamp'])




fig = plt.figure(figsize=(8, 6)) 
gs = gridspec.GridSpec(2,1, height_ratios=[3, 1]) 
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1], sharex=ax0)
RC.plot(y=['kw_energy_consumption','prediction'], ax = ax0)
RC.plot(y=['anomaly_likelihood'], ax=ax1)

fig.canvas.draw()



fig = plt.figure(figsize=(8, 6)) 
RC.plot(y=['kw_energy_consumption','prediction'])
RC['timestamp'] = RC['timestamp'].astype(int)
RC.index = RC.index.astype(str)
RC.plot(x = 'timestamp', y= 'kw_energy_consumption')
RC.plot(y = 'timestamp')





























