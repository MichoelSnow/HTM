# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 12:17:57 2017

@author: msnow1
"""

from nupic.encoders.date import DateEncoder
from nupic.encoders.random_distributed_scalar import \
    RandomDistributedScalarEncoder
#from nupic.encoders.scalar import ScalarEncoder

#import matplotlib.pyplot as plt
#from datetime import datetime
import numpy as np
np.set_printoptions(threshold=np.nan)
import pandas as pd


def organize_data(file_name):
    data_fl = pd.read_csv(file_name)
    col_types = data_fl.iloc[0][:]
    data_fl.drop([0,1],inplace =True)
    for i in data_fl.columns:
        if col_types.loc[i] == 'datetime':
            try:
                data_fl[i] = pd.to_datetime(data_fl[i], format = "%Y-%m-%d %H:%M:%S")
            except:
                data_fl[i] = pd.to_datetime(data_fl[i])
        elif col_types.loc[i] == 'float':
            data_fl[i] = pd.to_numeric(data_fl[i])
    data_fl = data_fl.reset_index(drop=True)
    return data_fl



def smart_encode(data_fl):
    encoder_list = []
    for i in data_fl.columns:        
        if data_fl[i].dtype == 'M8[ns]':
            time_delta = data_fl[i][1] - data_fl[i][0]
            if  time_delta >= pd.Timedelta(1,unit='M'):
                encoder_list += [[DateEncoder(season=(5,1))]]
            elif time_delta >= pd.Timedelta(1,unit='D'):
                encoder_list += [[DateEncoder(season=(21)),
                                  DateEncoder(dayOfWeek=(21,1)),
                                  DateEncoder(weekend=5)]]
            else:                
                encoder_list += [[DateEncoder(season=(5,1)),
                                  DateEncoder(dayOfWeek=(5,1)),
                                  DateEncoder(weekend=5),
                                  DateEncoder(timeOfDay=(5,1))]]
        if data_fl[i].dtype == "float":
            col_range = data_fl[i].max() - data_fl[i].min()
            res = col_range/(400-21)
            encoder_list += [[RandomDistributedScalarEncoder(res)]]
    return encoder_list
                            
def value_encoder(data_fl,encoder_list,enc_sz):
    encoding = []
    for i in xrange(enc_sz):#xrange(len(data_fl)):
        enc_array = []
        for jpos,j in enumerate(data_fl.columns):
            if data_fl[j].dtype == 'M8[ns]':
                for k in xrange(len(encoder_list[jpos])):
                    enc_array += [encoder_list[jpos][k].encode(data_fl[j][i])]
            elif data_fl[j].dtype == "float":
                enc_array += [encoder_list[jpos][0].encode(data_fl[j][i])]
        encoding += [np.concatenate(enc_array)]
    return encoding

def create_encoding(file_name):
    data_fl = organize_data(file_name)
    encoder_list = smart_encode(data_fl)
    encoding = value_encoder(data_fl,encoder_list,len(data_fl))
    return encoding

#file_name = "E:\\MyDocuments\\GitHub\\HTM\\AlgorithmComponents\\Data\\appt_htm_0steps.csv"
#output_name = "E:\\MyDocuments\\GitHub\\HTM\\AlgorithmComponents\\Data\\appt_htm_0steps_encoded.npy"



#plt.imshow(numpy.reshape(encoding[5][:240],(15,16)))


