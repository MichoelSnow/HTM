# -*- coding: utf-8 -*-
"""
Created on Thu May 11 07:57:46 2017

@author: msnow1
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.dates import date2num, DateFormatter
import os, os.path
import glob 

def lookup(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date:pd.to_datetime(date,errors='coerce') for date in s.unique()}
    return s.map(dates)


def HTMprep(DataFl,timeNm,VarNm):
    line = pd.DataFrame({timeNm:["datetime"," "],VarNm:["float"," "]},index=[0,1])
    return pd.concat([line, DataFl],join = 'inner',ignore_index =True)


# %%
# MTA Turnstile information

# Convert to a more useable form
DataDir = 'E:\\MyDocuments\\HTM\\DataSets\\MTA\\'
DataList = glob.glob1(DataDir, "*.txt")
DataList.sort()
Trnstl = None
for Ct,Nm in enumerate(DataList):
    CsvPth = "%s%s" % (DataDir, Nm)
    tmp = pd.read_csv(CsvPth)
    try:
        Trnstl = pd.concat([tmp,Trnstl])
    except:
        Trnstl = tmp

Trnstl = Trnstl.drop(['C/A','UNIT','DIVISION','DESC'],axis=1)
Trnstl.to_csv('E:\\MyDocuments\\HTM\\DataSets\\MTA\\Trnstle_Narrow.csv',index = False)

# %%

Trnstl['timestamp'] = Trnstl[['DATE', 'TIME']].apply(lambda x: ' '.join(x), axis=1)    
Trnstl = Trnstl.drop(['DATE','TIME'],axis=1)

Trnstl['timestamp'] = lookup(Trnstl['timestamp'])

# %%
Trnstl_dif = Trnstl
Trnstl_dif = Trnstl_dif.sort_values(['STATION','SCP','timestamp'])
Trnstl_dif = Trnstl_dif.rename(columns = {Trnstl_dif.columns[4]:'EXITS'})
Trnstl_dif['TmDif'] = Trnstl_dif['timestamp'] - Trnstl_dif['timestamp'].shift()
Trnstl_dif['EntriesDif'] = Trnstl_dif['ENTRIES'] - Trnstl_dif['ENTRIES'].shift()
Trnstl_dif['ExitsDif'] = Trnstl_dif['EXITS'] - Trnstl_dif['EXITS'].shift()
Trnstl_dif = Trnstl_dif.reset_index(drop=True)
Trnstl_dif = Trnstl_dif[Trnstl_dif.EntriesDif>=0]
Trnstl_dif = Trnstl_dif[:][Trnstl_dif['TmDif']==pd.Timedelta('4 hours')]
Trnstl_dif = Trnstl_dif.groupby(['timestamp','STATION'],as_index=False).sum()
Trnstl_dif = Trnstl_dif.sort_values(['STATION','timestamp'])
Trnstl_dif = Trnstl_dif.reset_index(drop=True)

# %%
Stnum = 41
Trnstl_dif3 = Trnstl_dif[Trnstl_dif.STATION == StNm[Stnum]]

Trnstl_dif3['dates'] = [date2num(date) for date in Trnstl_dif3['timestamp']]
MainGraph = Trnstl_dif3.plot(x = 'dates', y='EntriesDif', title = StNm[Stnum])
dateFormatter = DateFormatter('%m/%d')
MainGraph.xaxis.set_major_formatter(dateFormatter)

# %%

StNm = Trnstl_dif['STATION'].unique()
Trnstl_dif2 = Trnstl_dif[Trnstl_dif.STATION == StNm[Stnum]]

Trnstl_csv = HTMprep(Trnstl_dif2,'timestamp','EntriesDif')
csvNm = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\Generic\\Trnstl_%s.csv' % (StNm[Stnum].replace(" ", "_").replace("-", "_").replace("/", "_"))
Trnstl_csv.to_csv(csvNm, index=False)





# %%

Three11 = pd.read_csv('311_Service_Requests_2016_Narrow.csv')

Three11 = Three11.rename(columns = {'Created Date':'timestamp'})
Three11['counts'] = 1
Three11_Narrow = Three11[['counts','Agency']]
Three11_Narrow = Three11_Narrow.resample('H').sum()

Three11['timestamp'] = lookup(Three11['timestamp'])
Three11 = Three11.set_index('timestamp')

Three11_Narrow = Three11[['counts','Agency']]
Three11_Narrow = Three11_Narrow.resample('2H').sum()
Three11_Narrow.reset_index(level=0, inplace=True)

Three11_Narrow_csv = HTMprep(Three11_Narrow,'timestamp','counts')
Three11_Narrow_csv.to_csv('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Generic\\Three11_Narrow.csv', index=False)

# %%
Three11_Narrow = Three11[['counts','Agency']]
Three11_Narrow = Three11_Narrow.resample('2H').sum()
Three11_Narrow['dates'] = [date2num(date) for date in Three11_Narrow.index]
MainGraph = Three11_Narrow.plot(y='counts')
dateFormatter = DateFormatter('%m/%d')
MainGraph.xaxis.set_major_formatter(dateFormatter)


# %%


Park = pd.read_csv('Open_Parking_and_Camera_Violations_Narrow_2016.csv')

ParkCol = Park.columns
Park = Park.dropna(axis=0,how = 'any',subset = ['Issue Date','Violation Time'])
Park['timestamp'] = Park[['Issue Date', 'Violation Time']].apply(lambda x: ' '.join(x), axis=1)    

Park['counts'] = 1
Park_narrow = Park[['timestamp','counts']]
Park_narrow['timestamp'] = Park_narrow.timestamp.str.replace('P',' PM')
Park_narrow['timestamp'] = Park_narrow.timestamp.str.replace('A',' AM')
Park_narrow['timestamp'] = Park_narrow.timestamp.str.replace('+','0')


Park_narrow['timestamp'] = lookup(Park_narrow['timestamp'])
Park_narrow = Park_narrow[pd.notnull(Park_narrow.timestamp)]

Park_narrow_H = Park_narrow.resample('2H', on ='timestamp').sum()

# %%
Park_narrow = Park_narrow[Park_narrow.timestamp != '07/08/2016 28:20P']
Park_narrow = Park_narrow[~Park_narrow['timestamp'].isin(['+'])]
date = Park_narrow.timestamp.unique()
# %%
for i in range(len(Park_narrow)):
    #a = Park_narrow.timestamp[i]
    pd.to_datetime(date[i])

# %%




# 7930830

