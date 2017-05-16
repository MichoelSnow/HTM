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
FndngFull = pd.read_csv('E:\MyDocuments\HTM\Health.csv', na_values="", 
                     header = None) 
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





























