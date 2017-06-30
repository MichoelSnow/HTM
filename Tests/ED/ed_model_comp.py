# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:05:16 2017

@author: msnow1
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.dates import date2num, DateFormatter
from statsmodels.tsa import ar_model

def MSE(Vals,Pred,WndwDys,DyStps):
    Resid = (abs(Pred - Vals))**2/(WndwDys*DyStps)
    return Resid.rolling(WndwDys*DyStps,center=False).sum()

# %% HTM Prediction

WndwDys = 30
DyStps = 8

InputName = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ed_3h_out_24steps.csv'
ed_3h_htm = pd.read_csv(InputName, na_values="",index_col=0,usecols=[0,1,2])
ed_3h_htm.index = pd.to_datetime(ed_3h_htm.index, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce') 
ed_3h_htm['MSE'] = MSE(ed_3h_htm.Ct,ed_3h_htm.prediction,WndwDys,DyStps)

ed_3h = pd.DataFrame(ed_3h_htm.prediction)
ed_3h.rename(columns = {"prediction":"HTM"},inplace=True)
ed_3h_mse = pd.DataFrame(ed_3h_htm.MSE)
ed_3h_mse.rename(columns = {"MSE":"HTM"},inplace=True)


# %% Mean Ct over past 30 days per time step
ed_3h_mn = ed_3h_htm[['Ct']]
ed_3h_mn['prediction']=0
for i in range(0,24,3):
    ed_3h_mn.loc[ed_3h_mn.index.hour == i,'prediction'] = \
    ed_3h_mn.loc[ed_3h_mn.index.hour == i,'Ct'].rolling(WndwDys,center=False).mean()    
ed_3h_mn['MSE'] = MSE(ed_3h_mn.Ct,ed_3h_mn.prediction,WndwDys,DyStps)

ed_3h['RollMn'] = ed_3h_mn.prediction
ed_3h_mse['RollMn'] = ed_3h_mn.MSE

# %% AR Model
ed_3h_ar = ed_3h_htm[['Ct']]
ar_mdl = ar_model.AR(ed_3h_ar)
ar_fit = ar_mdl.fit(maxlag=(5*DyStps))
aa = ar_fit.predict()

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














# %% ED DATA SET

ED = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ERVisitsTriaged.csv', na_values="") 
ED.TRIAGED = pd.to_datetime(ED.TRIAGED, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
ED = ED[pd.notnull(ED.TRIAGED)]
ED = ED[:][ED.TRIAGED <= '2017/06/27']
ED = ED[:][ED.TRIAGED >= '1997/03/15']
ED['Ct'] = 1
ed_3h = ED.resample('3H',on ="TRIAGED").sum()
ed_3h = ed_3h.fillna(0)



# %% HTM Prediction

ed_3h_htm = pd.read_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\ED\\ed_3h_out_24steps.csv', 
                        na_values="",index_col=0,usecols=[0,1,2]) 
ed_3h['HTM'] = ed_3h_htm.prediction
ed_3h_htm['Resid'] = (abs(ed_3h_htm.prediction - ed_3h_htm.Ct))**2/(WndwDys*DyStps)
ed_3h_htm['MSE'] = ed_3h_htm.Resid.rolling(WndwDys*DyStps,center=False).sum()
ed_3h_mse['HTM'] = ed_3h_htm.MSE
