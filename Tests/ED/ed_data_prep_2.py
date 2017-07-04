# -*- coding: utf-8 -*-
"""
Created on Mon Jul 03 18:42:04 2017

@author: BJ
"""

import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib import gridspec
from matplotlib.dates import date2num, DateFormatter


ED = pd.read_csv('E:\Datasets\ERVisitsWide2010to2017.csv')
ED.TRIAGED = pd.to_datetime(ED.TRIAGED,format="%Y-%m-%d %H:%M:%S",errors ="coerce")
ED = ED[ED.TRIAGED<'2017-07-04']

ED_Fac1 = ED[ED.FACILITYID == 1]

ED_Fac1['Ct'] = 1
ED_Fac1_peds = ED_Fac1[['TRIAGED','Ct']][ED_Fac1.AGE<18]

# %%
ED_Fac1_peds_3h = ED_Fac1_peds.resample('2H',on = 'TRIAGED').sum()
ED_Fac1_peds_3h['dates'] = [date2num(date) for date in ED_Fac1_peds_3h.index]


MainGraph = ED_Fac1_peds_3h.plot(x = 'dates', y='Ct')
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)


# %%

 