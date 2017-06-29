# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:05:16 2017

@author: msnow1
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.dates import date2num, DateFormatter
# %% ED DATA SET

ED = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ERVisitsTriaged.csv', na_values="") 
ED.TRIAGED = pd.to_datetime(ED.TRIAGED, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
ED = ED[pd.notnull(ED.TRIAGED)]
ED = ED[:][ED.TRIAGED <= '2017/06/27']
ED = ED[:][ED.TRIAGED >= '1997/03/15']
ED['Ct'] = 1
ed_3h = ED.resample('3H',on ="TRIAGED").sum()
ed_3h = ed_3h.fillna(0)

WndwDys = 30
DyStps = 8

# %% Mean Ct over past 30 days per time step
ed_3h_mn = ed_3h[['Ct']]
ed_3h_mn['RollMn']=0
for i in range(0,24,3):
    ed_3h_mn.loc[ed_3h_mn.index.hour == i,'RollMn'] = \
    ed_3h_mn.loc[ed_3h_mn.index.hour == i,'Ct'].rolling(WndwDys,center=False).mean()
ed_3h['RollMn'] = ed_3h_mn.RollMn
ed_3h_mn.fillna(0,inplace=True)
ed_3h_mn['Resid'] = (abs(ed_3h_mn.RollMn - ed_3h_mn.Ct))**2/(WndwDys*DyStps)
ed_3h_mn.Resid.loc[ed_3h_mn.RollMn==0]=float('Nan')
ed_3h_mn['MSE'] = ed_3h_mn.Resid.rolling(WndwDys*DyStps,center=False).sum()

ed_3h_mse = pd.DataFrame(ed_3h_mn.MSE)
ed_3h_mse.rename(columns = {"MSE":"RollMn"},inplace=True)


# %% HTM Prediction

ed_3h_htm = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ed_3h_out_24steps.csv', 
                        na_values="",index_col=0,usecols=[0,1,2]) 
ed_3h['HTM'] = ed_3h_htm.prediction
ed_3h_htm['Resid'] = (abs(ed_3h_htm.prediction - ed_3h_htm.Ct))**2/(WndwDys*DyStps)
ed_3h_htm['MSE'] = ed_3h_htm.Resid.rolling(WndwDys*DyStps,center=False).sum()
ed_3h_mse['HTM'] = ed_3h_htm.MSE


# %% Plot
ed_3h['dates'] = [date2num(date) for date in ed_3h.index]
ed_3h_mse['dates'] = [date2num(date) for date in ed_3h_mse.index]
gs = gridspec.GridSpec(2,1, height_ratios=[3, 1]) 
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1], sharex=ax0)
MainGraph = ed_3h.plot(x = 'dates',y = ['Ct','RollMn','HTM'], ax = ax0)
AnomalyGraph = ed_3h_mse.plot(x = 'dates', y=['RollMn','HTM'], ax=ax1)
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)    
AnomalyGraph.xaxis.set_major_formatter(dateFormatter)
ax1.set_xlabel('Dates')
ax1.set_ylabel('MSE')
ax0.set_ylabel('Traige Cts')

