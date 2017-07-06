# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

os.chdir('E:/MyDocuments/GitHub/HTM/Tests/Appts/')
InputName = 'appt_htm_0steps.csv'


# %%
"""
Groups together code used for creating a NuPIC model and dealing with IO.
(This is a component of the One Hot Gym Anomaly Tutorial.)
"""

import sys
import csv
import datetime
import os
import getpass
os.environ["USER"] = getpass.getuser()
import pandas as pd
import numpy as np
#import importlib
import imp



from nupic.frameworks.opf.model_factory import ModelFactory
from nupic.data.inference_shifter import InferenceShifter

from HTMPkg.model_params_generic import GenericParams
from HTMPkg import output_anomaly_generic

DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the gym into the model. Results\n"
  "are written to an output file (default) "
)

DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"
# '7/2/10 0:00'
#DATE_FORMAT = "%m/%d/%y %H:%M"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"






def getNewParams(InputName):
    """
    
    """
    INPUT_FILE = "%s.csv" % (InputName)
    CsvData = pd.read_csv(INPUT_FILE)
    CsvCol = CsvData.columns
    CsvDataTypes = CsvData.loc[0].tolist()
    CsvData = CsvData[:][2:]
    csvMax,csvMin,csvStd = [],[],[]
    for Col,ColType in enumerate(CsvDataTypes):
        if ColType == 'float':
            CsvData[CsvCol[Col]] = pd.to_numeric(CsvData[CsvCol[Col]])
            csvMax.append(CsvData[CsvCol[Col]].max())
            csvMin.append(CsvData[CsvCol[Col]].min())
            csvStd.append(np.std(CsvData[CsvCol[Col]]))
        else:
            csvMax.append(None)
            csvMin.append(None)
            csvStd.append(None)
    return [CsvCol,CsvDataTypes,CsvData,csvMin,csvMax,csvStd]


def _fixupRandomEncoderParams(params, CsvCol, CsvDataTypes, CsvData, csvMin,
                              csvMax ,csvStd, minResolution):
    """
    Given model params, figure out the correct parameters for the
    RandomDistributed encoder. Modifies params in place.
    """
    encDict = (params["modelConfig"]["modelParams"]["sensorParams"]["encoders"])
    numBuckets = 130.0
    for Col,ColType in enumerate(CsvDataTypes):
        if ColType == 'datetime':
            Nm1 = '%s_timeOfDay' % (CsvCol[Col])
            encDict[Nm1] = {}
            encDict[Nm1]['type'] = 'DateEncoder'
            encDict[Nm1]['timeOfDay'] = [21,9.49]
            encDict[Nm1]['fieldname'] = CsvCol[Col]
            encDict[Nm1]['name'] = CsvCol[Col]
            Nm2 = '%s_dayOfWeek' % (CsvCol[Col])
            encDict[Nm2] = None
            Nm3 = '%s_weekend' % (CsvCol[Col])
            encDict[Nm3] = None
        elif ColType == 'float':
            encDict[CsvCol[Col]] = {}
            encDict[CsvCol[Col]]['name'] = CsvCol[Col]
            encDict[CsvCol[Col]]['fieldname'] = CsvCol[Col]
            encDict[CsvCol[Col]]['seed'] = 42
            encDict[CsvCol[Col]]["type"] =  "RandomDistributedScalarEncoder"
            maxVal = csvMax[Col]
            minVal = csvMin[Col]
            # Handle the corner case where the incoming min and max are the same
            if minVal == maxVal:
                maxVal = minVal + 1
            maxVal = maxVal
            minVal = minVal
            resolution = max(minResolution,(maxVal - minVal) / numBuckets)
            encDict[CsvCol[Col]]["resolution"] = resolution
#  for encoder in encodersDict.itervalues():
#    if encoder is not None:
#      if encoder["type"] == "RandomDistributedScalarEncoder": 
#        resolution = max(minResolution,
#                         (maxVal - minVal) / encoder.pop("numBuckets")
#                        )
#        encodersDict["c1"]["resolution"] = resolution

#

def getModelParamsFromName(InputName):
    """
    Given a gym name, assumes a matching model params python module exists 
    within the model_params directory and attempts to import it.
    :param gymName: Gym name, used to guess the model params module name.
    :return: OPF Model params dictionary
    """
    #print os.getcwd()
#    importName = "model_params.%s_model_params" % (InputName.replace(" ", "_").replace("-", "_"))
    importName = "%s_model_params" % (InputName.replace(" ", "_").replace("-", "_"))
    importPath = "%s\\model_params\\%s_model_params.py" %(os.getcwd(),InputName.replace(" ", "_").replace("-", "_"))
    importedModelParams = imp.load_source(importName,importPath).MODEL_PARAMS
#    importedModelParams = importlib.import_module(importName,os.getcwd()).MODEL_PARAMS
    params = {'modelConfig': importedModelParams}
    return params

def createModel(InputName):
    """
    Given a model params dictionary, create a CLA Model. Automatically enables
    inference for predicted field.
    :param modelParams: Model params dict
    :return: OPF Model object
    """
    CsvCol,CsvDataTypes,CsvData,csvMin,csvMax,csvStd = getNewParams(InputName)
    # Try to find already existing params file
    try:
        params = getModelParamsFromName(InputName)
        steps = int(params["modelConfig"]["modelParams"]["clParams"]["steps"])
        params["inferenceArgs"] = {'inputPredictedField':'auto',
            'predictionSteps': [steps],'predictedField': CsvCol[1]}
        print 'swarm file found, using given values'
    except:    
        print 'swarm file NOT found, using generic values'
        minResolution = 0.001
        tmImplementation = "cpp"
        # Load model parameters and update encoder params
        params = GenericParams(tmImplementation)      
        _fixupRandomEncoderParams(params, CsvCol, CsvDataTypes, CsvData,
                                csvMin, csvMax, csvStd, minResolution)
  
    params["inferenceArgs"]["predictedField"] = CsvCol[1]
    params['modelConfig']['modelParams']['clEnable'] = True
    model = ModelFactory.create(modelConfig=params["modelConfig"])
    model.enableLearning()  
    model.enableInference(params["inferenceArgs"])
    return model