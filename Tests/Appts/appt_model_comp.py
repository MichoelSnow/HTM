# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 12:38:18 2017

@author: msnow1
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:05:16 2017

@author: msnow1
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.dates import date2num, DateFormatter
from statsmodels.tsa import ar_model, arima_model


def MSE(Vals,Pred,WndwDys,DyStps):
    Resid = (abs(Pred - Vals))**2/(WndwDys*DyStps)
    return Resid.rolling(WndwDys*DyStps,center=False).sum()

# %% HTM Prediction

WndwDys = 30
DyStps = 1
PredAhead = 3

InputName = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\appts\\appt_htm_3steps_out.csv'
appt_htm = pd.read_csv(InputName, na_values="",index_col=0,usecols=[0,1,2])
appt_htm.index = pd.to_datetime(appt_htm.index, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce') 
appt_htm['MSE'] = MSE(appt_htm.Ct,appt_htm.prediction,WndwDys,DyStps)

#ed_3h = pd.DataFrame(ed_3h_htm.prediction)
appt = appt_htm[['Ct','prediction']]
appt.rename(columns = {"prediction":"HTM"},inplace=True)
appt_mse = pd.DataFrame(appt_htm.MSE)
appt_mse.rename(columns = {"MSE":"HTM"},inplace=True)


# %% Mean Ct over past 30 days per time step
appt_mn = appt_htm[['Ct']]
appt_mn['prediction'] = appt_mn.Ct.rolling(WndwDys,center=False).mean()
appt_mn.prediction = appt_mn.prediction.shift(PredAhead*DyStps)
appt_mn['MSE'] = MSE(appt_mn.Ct,appt_mn.prediction,WndwDys,DyStps)

appt['RollMn'] = appt_mn.prediction
appt_mse['RollMn'] = appt_mn.MSE

# %% AR Model
appt_ar = appt_htm[['Ct']]
ar_mdl = ar_model.AR(appt_ar)
ar_fit = ar_mdl.fit(maxlag=(WndwDys*DyStps))
appt_ar['prediction'] = ar_fit.predict()
appt_ar['MSE'] = MSE(appt_ar.Ct,appt_ar.prediction,WndwDys,DyStps)


appt['AR'] = appt_ar.prediction
appt_mse['AR'] = appt_ar.MSE



# %% Plot
appt['dates'] = [date2num(date) for date in appt.index]
appt_mse['dates'] = [date2num(date) for date in appt_mse.index]
gs = gridspec.GridSpec(2,1, height_ratios=[3, 1]) 
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1], sharex=ax0)
ax0.set_prop_cycle('color',['b', 'orange','g','r'])
ax1.set_prop_cycle('color',['orange','g','r'])
MainGraph = appt.plot(x = 'dates',y = ['Ct','RollMn','HTM','AR'], ax = ax0)
AnomalyGraph = appt_mse.plot(x = 'dates', y=['RollMn','HTM','AR'], ax=ax1)
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)    
AnomalyGraph.xaxis.set_major_formatter(dateFormatter)
ax1.set_xlabel('Dates')
ax1.set_ylabel('MSE')
ax0.set_ylabel('Traige Cts')




# %%
InputName = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\appts\\appt_htm_3steps_out - Copy.csv'
appt_htm1 = pd.read_csv(InputName, na_values="",index_col=0,usecols=[0,2])
InputName = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\appts\\appt_htm_3steps_out.csv'
appt_htm2 = pd.read_csv(InputName, na_values="",index_col=0,usecols=[0,2])
appt_htm2['pred20'] = appt_htm1.prediction



