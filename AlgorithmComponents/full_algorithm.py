# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 14:38:53 2017

@author: msnow1
"""

from nupic.encoders.date import DateEncoder
from nupic.encoders.random_distributed_scalar import \
    RandomDistributedScalarEncoder
from nupic.algorithms.spatial_pooler import SpatialPooler
from nupic.algorithms.temporal_memory import TemporalMemory
from nupic.algorithms.sdr_classifier_factory import SDRClassifierFactory
    
#from nupic.encoders.scalar import ScalarEncoder

#import matplotlib.pyplot as plt
#from datetime import datetime
import numpy as np
np.set_printoptions(threshold=np.nan)
import pandas as pd
import os
import getpass
os.environ["USER"] = getpass.getuser()





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
    encoder_width = 0
    for i in data_fl.columns:        
        if data_fl[i].dtype == 'M8[ns]':
            time_delta = data_fl[i][1] - data_fl[i][0]
            if  time_delta >= pd.Timedelta(1,unit='M'):
                encoder_list += [[DateEncoder(season=21)]]
                encoder_width += sum(x.getWidth() for x in encoder_list[-1])
            elif time_delta >= pd.Timedelta(1,unit='D'):
                encoder_list += [[DateEncoder(season=(21)),
                                  DateEncoder(dayOfWeek=(21,1)),
                                  DateEncoder(weekend=5)]]
                encoder_width += sum(x.getWidth() for x in encoder_list[-1])
            else:                
                encoder_list += [[DateEncoder(season=21),
                                  DateEncoder(dayOfWeek=(5,1)),
                                  DateEncoder(weekend=5),
                                  DateEncoder(timeOfDay=(5,1))]]
                encoder_width += sum(x.getWidth() for x in encoder_list[-1])
        if data_fl[i].dtype == "float":
            col_range = data_fl[i].max() - data_fl[i].min()
            res = col_range/(400-21)
            encoder_list += [[RandomDistributedScalarEncoder(res)]]
            encoder_width += sum(x.getWidth() for x in encoder_list[-1])
    return encoder_list, encoder_width

def smart_encode2(data_fl):
    encoder_list = []
    encoder_width = 0
    for i in data_fl.columns:        
        if data_fl[i].dtype == 'M8[ns]':
            time_delta = data_fl[i][1] - data_fl[i][0]
            if  time_delta >= pd.Timedelta(1,unit='M'):
                encoder_list += [[DateEncoder(season=21)]]
                encoder_width += sum(x.getWidth() for x in encoder_list[-1])
            elif time_delta >= pd.Timedelta(1,unit='D'):
                encoder_list += [[DateEncoder(season=(21)),
                                  DateEncoder(dayOfWeek=(21,1)),
                                  DateEncoder(weekend=5)]]
                encoder_width += sum(x.getWidth() for x in encoder_list[-1])
            else:                
                encoder_list += [[DateEncoder(timeOfDay=(21,1)),
                                  DateEncoder(weekend=21)]]
                encoder_width += sum(x.getWidth() for x in encoder_list[-1])
        if data_fl[i].dtype == "float":
            col_range = data_fl[i].max() - data_fl[i].min()
            res = col_range/(400-21)
            encoder_list += [[RandomDistributedScalarEncoder(0.88)]]
            encoder_width += sum(x.getWidth() for x in encoder_list[-1])
    return encoder_list, encoder_width
                            
#def value_encoder(data_fl,encoder_list,enc_sz):
#    encoding = []
#    for i in xrange(enc_sz):#xrange(len(data_fl)):
#        enc_array = []
#        for jpos,j in enumerate(data_fl.columns):
#            if data_fl[j].dtype == 'M8[ns]':
#                for k in xrange(len(encoder_list[jpos])):
#                    enc_array += [encoder_list[jpos][k].encode(data_fl[j][i])]
#            elif data_fl[j].dtype == "float":
#                enc_array += [encoder_list[jpos][0].encode(data_fl[j][i])]
#        encoding += [np.concatenate(enc_array)]
#    return encoding

def create_sp(encoder_width):
    sp = SpatialPooler(
      # How large the input encoding will be.
      inputDimensions=(encoder_width),
      # How many mini-columns will be in the Spatial Pooler.
      columnDimensions=(2048),
      # What percent of the columns's receptive field is 
      # available for potential synapses?
      potentialPct=0.85,
      # This means that the input space has no topology.
      globalInhibition=True,
      localAreaDensity=-1.0,
      # Roughly 2%, giving that there is only one inhibition area because 
      # we have turned on globalInhibition (40 / 2048 = 0.0195)
      numActiveColumnsPerInhArea=40.0,
      # How quickly synapses grow and degrade.
      synPermInactiveDec=0.005,
      synPermActiveInc=0.04,
      synPermConnected=0.1,
      # boostStrength controls the strength of boosting. Boosting 
      # encourages efficient usage of SP columns.
      boostStrength=3.0,
      # Random number generator seed.
      seed=1956,
      # Determines if inputs at the beginning and end of an input dimension 
      # should be considered neighbors when mapping columns to inputs.
      wrapAround=False)        
    return sp    
    

def create_tm():
    tm = TemporalMemory(
      # Must be the same dimensions as the SP
      columnDimensions=(2048, ),
      # How many cells in each mini-column.
      cellsPerColumn=32,
      # A segment is active if it has >= activationThreshold connected synapses
      # that are active due to infActiveState
      activationThreshold=16,
      initialPermanence=0.21,
      connectedPermanence=0.5,
      # Minimum number of active synapses for a segment to be considered during
      # search for the best-matching segments.
      minThreshold=12,
      # The max number of synapses added to a segment during learning
      maxNewSynapseCount=20,
      permanenceIncrement=0.1,
      permanenceDecrement=0.1,
      predictedSegmentDecrement=0.0,
      maxSegmentsPerCell=128,
      maxSynapsesPerSegment=32,
      seed=1960)        
    return tm



file_name = "E:\\MyDocuments\\GitHub\\HTM\\AlgorithmComponents\\Data\\appt_htm_0steps.csv"
file_name = "E:\\MyDocuments\\GitHub\\HTM\\AlgorithmComponents\\Data\\gymdata.csv"
data_fl = organize_data(file_name)    
encoder_list, encoder_width = smart_encode2(data_fl)   
sp = create_sp(encoder_width) 
tm = create_tm()
classifier = SDRClassifierFactory.create()
encoded_data, sp_output, tm_output = [], [], []
prediction, confidence = [],[]
for i in xrange(1):#xrange(len(data_fl)):
    enc_array = []
    for count,record in enumerate(data_fl.columns):
        if data_fl[record].dtype == 'M8[ns]':
            for k in xrange(len(encoder_list[count])):
                enc_array += [encoder_list[count][k].encode(data_fl[record][i])]
        elif data_fl[record].dtype == "float":
            enc_array += [encoder_list[count][0].encode(data_fl[record][i])]
    encoded_data += [np.concatenate(enc_array)]
    
    # Create an array to represent active columns, all initially zero. This
    # will be populated by the compute method below. It must have the same
    # dimensions as the Spatial Pooler.
    activeColumns = np.zeros(2048)
    sp.compute(encoded_data[-1], True, activeColumns)
    activeColumnIndices = np.nonzero(activeColumns)[0]
    sp_output += [activeColumnIndices]
    
    # Execute Temporal Memory algorithm over active mini-columns.
    tm.compute(activeColumnIndices, learn=True)
    activeCells = tm.getActiveCells()
    tm_output += [activeCells]
    
    # Get the bucket info for this input value for classification.
#    bucketIdx = encoder_list[1][0].getBucketIndices(data_fl.Ct[i])[0]
    bucketIdx = encoder_list[1][0].getBucketIndices(data_fl.iloc[i,1])[0]

    # Run classifier to translate active cells back to scalar value.
    classifierResult = classifier.compute(
      recordNum=i,
      patternNZ=activeCells,
      classification={
        "bucketIdx": bucketIdx,
#        "actValue": data_fl.Ct[i]
        "actValue": data_fl.iloc[i,1]
      },
      learn=True,
      infer=True
    )
    
    # Print the best prediction for 1 step out.
    probability, value = sorted(
      zip(classifierResult[1], classifierResult["actualValues"]),
      reverse=True
    )[0]
    prediction += [value]
    confidence += [probability*100]
    
    


  
    
    
    
    
    
    
    
    
    