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
PredAhead = 1

InputName = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\PredictionCheck\\appt_htm_1steps_out.csv'
pred_htm = pd.read_csv(InputName, na_values="",index_col=0,usecols=[0,1,2])
#pred_htm2.index = pd.to_datetime(pred_htm2.index, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce') 
pred_htm.index = pd.to_datetime(pred_htm.index) 
pred_htm['MSE'] = MSE(pred_htm.Ct,pred_htm.prediction,WndwDys,DyStps)

#ed_3h = pd.DataFrame(ed_3h_htm.prediction)
pred = pred_htm[['Ct','prediction']]
pred.rename(columns = {"prediction":"HTM"},inplace=True)
pred_mse = pd.DataFrame(pred_htm.MSE)
pred_mse.rename(columns = {"MSE":"HTM"},inplace=True)



# %% Mean Ct over past 30 days per time step
pred_mn = pred_htm[['Ct']]
pred_mn['prediction'] = pred_mn.Ct.rolling(WndwDys,center=False).mean()
pred_mn.prediction = pred_mn.prediction.shift(PredAhead*DyStps)
pred_mn['MSE'] = MSE(pred_mn.Ct,pred_mn.prediction,WndwDys,DyStps)

pred['RollMn'] = pred_mn.prediction
pred_mse['RollMn'] = pred_mn.MSE

# %% AR Model
pred_ar = pred_htm[['Ct']]
ar_mdl = ar_model.AR(pred_ar)
ar_fit = ar_mdl.fit(maxlag=(WndwDys*DyStps))
pred_ar['prediction'] = ar_fit.predict()
pred_ar['MSE'] = MSE(pred_ar.Ct,pred_ar.prediction,WndwDys,DyStps)


pred['AR'] = pred_ar.prediction
pred_mse['AR'] = pred_ar.MSE

# %% HTM Prediction

InputName = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\PredictionCheck\\gymdata_out.csv'
pred_htm = pd.read_csv(InputName, na_values="",index_col=0,usecols=[0,1,2])
#pred_htm.index = pd.to_datetime(pred_htm.index, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce') 
pred_htm.index = pd.to_datetime(pred_htm.index) 
pred_htm['MSE'] = MSE(pred_htm.Ct,pred_htm.prediction,WndwDys,DyStps)

#ed_3h = pd.DataFrame(ed_3h_htm.prediction)
pred['HTM1v'] = pred_htm.prediction
pred_mse['HTM1v'] = pred_htm.MSE

# %% HTM Prediction

InputName = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\PredictionCheck\\pred_htm_cheat_out.csv'
pred_htm_cheat = pd.read_csv(InputName, na_values="",index_col=0,usecols=[0,1,2])
#pred_htm.index = pd.to_datetime(pred_htm.index, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce') 
pred_htm_cheat.index = pd.to_datetime(pred_htm_cheat.index) 
pred_htm_cheat['MSE'] = MSE(pred_htm_cheat.Ct,pred_htm_cheat.prediction,WndwDys,DyStps)

#ed_3h = pd.DataFrame(ed_3h_htm.prediction)
pred['HTMcheat'] = pred_htm_cheat.prediction
pred_mse['HTMcheat'] = pred_htm_cheat.MSE

# %%

pred['dates'] = [date2num(date) for date in pred.index]
pred_mse['dates'] = [date2num(date) for date in pred_mse.index]
gs = gridspec.GridSpec(2,1, height_ratios=[3, 1]) 
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1], sharex=ax0)
ax0.set_prop_cycle('color',['b', 'orange','g','r'])
ax1.set_prop_cycle('color',['orange','g','r'])
MainGraph = pred.plot(x = 'dates',y = ['Ct','RollMn','HTM','AR'], ax = ax0)
AnomalyGraph = pred_mse.plot(x = 'dates', y=['RollMn','HTM','AR'], ax=ax1)
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)    
AnomalyGraph.xaxis.set_major_formatter(dateFormatter)
ax1.set_xlabel('Dates')
ax1.set_ylabel('MSE')
ax0.set_ylabel('Traige Cts')
MainGraph.legend(tuple(['Show up','Rolling Mean','HTM','Auto Regression']), loc=1)
AnomalyGraph.legend(tuple(['Rolling Mean','HTM','Auto Regression']), loc=1)

# %% Plot
pred['dates'] = [date2num(date) for date in pred.index]
pred_mse['dates'] = [date2num(date) for date in pred_mse.index]
gs = gridspec.GridSpec(2,1, height_ratios=[3, 1]) 
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1], sharex=ax0)
ax0.set_prop_cycle('color',['b', 'orange','g','r'])
ax1.set_prop_cycle('color',['orange','g','r'])
MainGraph = pred.plot(x = 'dates',y = ['Ct','HTM','HTM2v','HTMcheat'], ax = ax0)
AnomalyGraph = pred_mse.plot(x = 'dates', y=['HTM1v','HTM2v','HTMcheat'], ax=ax1)
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)    
AnomalyGraph.xaxis.set_major_formatter(dateFormatter)
ax1.set_xlabel('Dates')
ax1.set_ylabel('MSE')
ax0.set_ylabel('Cts')
#MainGraph.legend(tuple(['Show up','Rolling Mean','HTM','Auto Regression']), loc=1)
#AnomalyGraph.legend(tuple(['Rolling Mean','HTM','Auto Regression']), loc=1)




# %%
InputName = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\appts\\appt_htm_3steps_out - Copy.csv'
appt_htm1 = pd.read_csv(InputName, na_values="",index_col=0,usecols=[0,2])
InputName = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\appts\\appt_htm_3steps_out.csv'
appt_htm2 = pd.read_csv(InputName, na_values="",index_col=0,usecols=[0,2])
appt_htm2['pred20'] = appt_htm1.prediction



