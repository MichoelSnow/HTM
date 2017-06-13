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
from pkg_resources import resource_stream
import json
import importlib

from nupic.frameworks.opf.modelfactory import ModelFactory
#from nupic.frameworks.opf.common_models.cluster_params import (
#  getScalarMetricWithTimeOfDayAnomalyParams)



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
    importName = "model_params.%s_model_params" % (InputName.replace(" ", "_").
                                                   replace("-", "_"))
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
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
        params["inferenceArgs"] = {'inputPredictedField':'auto',
            'predictionSteps': [1],'predictedField': CsvCol[1]}
    except:    
        print 'swarm file not found, using generic values'
  # Get the new parameters from the csv file
        minResolution = 0.001
        tmImplementation = "cpp"
        # Load model parameters and update encoder params
        if (tmImplementation is "cpp"):
            paramFileRelativePath = os.path.join(
            "anomaly_params_random_encoder",
            "best_single_metric_anomaly_params_cpp.json")
        elif (tmImplementation is "tm_cpp"):
            paramFileRelativePath = os.path.join(
            "anomaly_params_random_encoder",
            "best_single_metric_anomaly_params_tm_cpp.json")
        else:
            raise ValueError("Invalid string for tmImplementation. \
                         Try cpp or tm_cpp")
        
        with resource_stream(__name__, paramFileRelativePath) as infile:
            params = json.load(infile)  
      
        _fixupRandomEncoderParams(params, CsvCol, CsvDataTypes, CsvData,
                                csvMin, csvMax, csvStd, minResolution)
  
    params["inferenceArgs"]["predictedField"] = CsvCol[1]
    params['modelConfig']['modelParams']['clEnable'] = True
    model = ModelFactory.create(modelConfig=params["modelConfig"])
    model.enableLearning()  
    model.enableInference(params["inferenceArgs"])
    return model





def runIoThroughNupic(inputData, model, InputName):
  """
  Handles looping over the input data and passing each row into the given model
  object, as well as extracting the result object and passing it into an output
  handler.
  :param inputData: file path to input data CSV
  :param model: OPF Model object
  :param InputName: Gym name, used for output handler naming
  """
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows     
  ColNm = csvReader.next()
  csvReader.next()
  csvReader.next()

  output = output_anomaly_generic.NuPICFileOutput(InputName)

  counter = 0
  for row in csvReader:
    counter += 1
    if (counter % 100 == 0):
      print "Read %i lines..." % counter
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    PredFld = [float(row[Ct]) for Ct in xrange(1,len(ColNm))]
    ResDict = {ColNm[x] : PredFld[x-1] for x in xrange(1,len(ColNm))}
    ResDict["timestamp"] = timestamp
    result = model.run(ResDict)


    prediction = result.inferences["multiStepBestPredictions"][1]
    anomalyScore = result.inferences["anomalyScore"]
    output.write(timestamp, PredFld[0], prediction, anomalyScore)

  inputFile.close()
  output.close()


# %%
def runModel(InputName):
  """
  Assumes the gynName corresponds to both a like-named model_params file in the
  model_params directory, and that the data exists in a like-named CSV file in
  the current directory.
  :param InputName: Important for finding model params and input CSV file
  """
  print "Creating model from %s..." % InputName 
  model = createModel(InputName)
  inputData = "%s/%s.csv" % (DATA_DIR, InputName.replace(" ", "_"))
  runIoThroughNupic(inputData, model, InputName)

# %%

if __name__ == "__main__":
  print DESCRIPTION
  args = sys.argv[1:]  
  if args[0][-4:] == '.csv':
      InputName = args[0][:-4]   
  try: 
      InputName
  except NameError:
      raise ValueError('Need to enter the name of a csv file as an argument')
  runModel(InputName)