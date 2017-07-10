# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 09:54:21 2017

@author: msnow1
"""

import pandas as pd
from matplotlib.dates import date2num, DateFormatter
import numpy as np
import datetime as dt
import csv


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

def DataSplit2(DataFl, variable, bin_sz):
    var_min = DataFl[variable].min()
    var_max = DataFl[variable].max()
    for i in range(var_min,var_max,bin_sz):
        var_nm = '%s_%d_%d' % variable,i,i+bin_sz
        print var_nm
#        DataFl[Names[i]] = ((DataFl[Variable]>=Ranges[i][0]) & (DataFl[Variable]<=Ranges[i][1])).astype(int) 
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

#rw_ct = 10**6
#appt = pd.read_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_raw_2007_2015_dob_zip_fac_dept_type_create.csv', na_values="", nrows = rw_ct)
appt = pd.read_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_raw_2007_2015_dob_zip_fac_dept_type_create.csv', na_values="")
appt = appt.dropna()
appt_status = (appt.APPTSTATUSID == 1) | (appt.APPTSTATUSID == 14) | (appt.APPTSTATUSID == 4) | (appt.APPTSTATUSID == 13)
appt = appt[appt_status]
appt.APPOINTMENTDATETIME = pd.to_datetime(appt.APPOINTMENTDATETIME, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt.APPTCREATEDDATE = pd.to_datetime(appt.APPTCREATEDDATE, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt.DOB = pd.to_datetime(appt.DOB, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt = appt[appt.DOB < appt.APPTCREATEDDATE]
appt = appt[appt.APPTCREATEDDATE < appt.APPOINTMENTDATETIME]




appt_new = pd.DataFrame(appt.APPOINTMENTDATETIME)
appt_new['Ct'] = 1
appt_new['SHOW'] = ((appt.APPTSTATUSID == 1) | (appt.APPTSTATUSID == 14)).astype(int)
appt_new['AGE'] = ((appt.APPOINTMENTDATETIME - appt.DOB).astype('<m8[Y]')).astype(int)
appt_new['DIST'] = ((appt.APPOINTMENTDATETIME - appt.APPTCREATEDDATE).astype('<m8[D]')).astype(int)


appt.ZIPCODE = appt.ZIPCODE.str.slice(start=0,stop=5)
zip_large = appt.ZIPCODE.value_counts()[appt.ZIPCODE.value_counts() > .01*len(appt)]
for i in zip_large.index:
    appt_new['Z'+i] = (appt.ZIPCODE == i).astype(int)
appt.FACILITYID = appt.FACILITYID.astype(int)
fac_large = appt.FACILITYID.value_counts()[appt.FACILITYID.value_counts() > .01*len(appt)]
for i in fac_large.index:
    appt_new['F'+str(i)] = (appt.FACILITYID == i).astype(int)
dept_large = appt.ACADEMICSECTIONID.value_counts()[appt.ACADEMICSECTIONID.value_counts() > .01*len(appt)]
for i in dept_large.index:
    appt_new['D'+str(int(i))] = (appt.ACADEMICSECTIONID == i).astype(int)
    
age_ranges = [[0,17],[18,35],[36,54],[55,70],[71,120]]
age_names = ['AGE_0_17','AGE_18_35','AGE_36_54','AGE_55_70','AGE_71_120']
appt_new = DataSplit(appt_new,'AGE',age_ranges,age_names)
dist_ranges = [[0,30],[31,60],[61,90],[91,120],[120,365]]
dist_names = ['DIST_0_30','DIST_31_60','DIST_61_90','DIST_91_120','DIST_120_365']
appt_new = DataSplit(appt_new,'DIST',dist_ranges,dist_names)
appt_new = appt_new.drop(['DIST','AGE'],axis=1)


appt_agg = appt_new.resample('D',on='APPOINTMENTDATETIME').sum()
appt_agg = appt_agg.div(appt_agg.Ct,axis=0)
appt_agg.to_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_D_2007_2015_wide.csv')
# %%

appt_agg['dates'] = [date2num(date) for date in appt_agg.index]
col_nm = appt_agg.columns
MainGraph = appt_agg.plot(x='dates',y=['SHOW',col_nm[24],col_nm[25],col_nm[26],col_nm[27]])
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)  
#MainGraph.legend(tuple(['Show up',col_nm[2],col_nm[3],col_nm[4],col_nm[5],col_nm[6]]), loc=1)
MainGraph.legend( loc=1)
MainGraph.set_xlabel('Dates')
MainGraph.set_ylabel('Percent')
# %% Separate Data by Facility

filename = 'E:\\MyDocuments\\HospAgg\\Appts\\appt_raw_2007_2015_dob_zip_fac_dept_type_create.csv'
rw_ct = (sum(1 for row in open(filename)))



FacId = pd.read_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_raw_2007_2015_dob_zip_fac_dept_type_create.csv', na_values="", usecols=["FACILITYID"])
FacId = FacId.dropna()

#FacId.FACILITYID = FacId.FACILITYID.astype(int)
fac_large = FacId.FACILITYID.value_counts()[FacId.FACILITYID.value_counts() > .01*len(FacId)]
#i = fac_large.index[0]
#skip_rws = (FacId.index[FacId.FACILITYID!=fac_large.index[0]]+1).tolist()
for i in fac_large.index[1:]:    
    skip_rws = (FacId.index[FacId.FACILITYID!=i]+1).tolist()
    FacId_skp = pd.read_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_raw_2007_2015_dob_zip_fac_dept_type_create.csv', na_values="", skiprows = skip_rws)
    output_nm = 'E:\\MyDocuments\\HospAgg\\Appts\\appt_raw_2007_2015_fac%s.csv' % int(i)
    FacId_skp.to_csv(output_nm,index=False)


# %% Facility specific files

fac_id = 47
fl_nm = 'E:\\MyDocuments\\HospAgg\\Appts\\appt_raw_2007_2015_fac%d.csv' % fac_id
appt = pd.read_csv(fl_nm, na_values="")
appt = appt.dropna()
appt_status = (appt.APPTSTATUSID == 1) | (appt.APPTSTATUSID == 14) | (appt.APPTSTATUSID == 4) | (appt.APPTSTATUSID == 13)
appt = appt[appt_status]
appt.APPOINTMENTDATETIME = pd.to_datetime(appt.APPOINTMENTDATETIME, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt.APPTCREATEDDATE = pd.to_datetime(appt.APPTCREATEDDATE, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt.DOB = pd.to_datetime(appt.DOB, format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
appt = appt[appt.DOB < appt.APPTCREATEDDATE]
appt = appt[appt.APPTCREATEDDATE < appt.APPOINTMENTDATETIME]




appt_new = pd.DataFrame(appt.APPOINTMENTDATETIME)
appt_new['Ct'] = 1
appt_new['SHOW'] = ((appt.APPTSTATUSID == 1) | (appt.APPTSTATUSID == 14)).astype(int)
appt_new['AGE'] = ((appt.APPOINTMENTDATETIME - appt.DOB).astype('<m8[Y]')).astype(int)
appt_new['DIST'] = ((appt.APPOINTMENTDATETIME - appt.APPTCREATEDDATE).astype('<m8[D]')).astype(int)


appt.ZIPCODE = appt.ZIPCODE.str.slice(start=0,stop=5)
zip_large = appt.ZIPCODE.value_counts()[appt.ZIPCODE.value_counts() > .01*len(appt)]
for i in zip_large.index:
    appt_new['Z'+i] = (appt.ZIPCODE == i).astype(int)
dept_large = appt.ACADEMICSECTIONID.value_counts()[appt.ACADEMICSECTIONID.value_counts() > .05*len(appt)]
for i in dept_large.index:
    appt_new['D'+str(int(i))] = (appt.ACADEMICSECTIONID == i).astype(int)

aa = DataSplit2(appt_new,'AGE',10)
    
age_ranges = [[0,17],[18,35],[36,54],[55,70],[71,120]]
age_names = ['AGE_0_17','AGE_18_35','AGE_36_54','AGE_55_70','AGE_71_120']
appt_new = DataSplit(appt_new,'AGE',age_ranges,age_names)
dist_ranges = [[0,30],[31,60],[61,90],[91,120],[120,365]]
dist_names = ['DIST_0_30','DIST_31_60','DIST_61_90','DIST_91_120','DIST_120_365']
appt_new = DataSplit(appt_new,'DIST',dist_ranges,dist_names)
appt_new = appt_new.drop(['DIST','AGE'],axis=1)


appt_agg = appt_new.resample('D',on='APPOINTMENTDATETIME').sum()
appt_agg = appt_agg.div(appt_agg.Ct,axis=0)

appt_agg2 = appt_agg
appt_agg2 = appt_agg2.dropna()

#appt_agg.to_csv('E:\\MyDocuments\\HospAgg\\Appts\\appt_D_2007_2015_wide.csv')
# %%

appt_agg2['dates'] = [date2num(date) for date in appt_agg2.index]
col_nm = appt_agg2.columns
MainGraph = appt_agg2.plot(x='dates',y=['SHOW','DIST_0_30'])
dateFormatter = DateFormatter('%m/%d/%y')
MainGraph.xaxis.set_major_formatter(dateFormatter)  
#MainGraph.legend(tuple(['Show up',col_nm[2],col_nm[3],col_nm[4],col_nm[5],col_nm[6]]), loc=1)
MainGraph.legend( loc=1)
MainGraph.set_xlabel('Dates')
MainGraph.set_ylabel('Percent')













