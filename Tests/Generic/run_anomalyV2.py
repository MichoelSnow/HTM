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


from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.common_models.cluster_params import (
  getScalarMetricWithTimeOfDayAnomalyParams)

import nupic_anomaly_output


DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the gym into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
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
    CsvData = pd.read_csv(INPUT_FILE)
    CsvCol = CsvData.columns
    CsvData = CsvData[:][2:]
    CsvData[CsvCol[1]] = pd.to_numeric(CsvData[CsvCol[1]])
    csvMax = (CsvData[CsvCol[1]].max())
    csvMin = (CsvData[CsvCol[1]].min())
    return [CsvCol[1],CsvData,csvMin,csvMax]




def createModel(InputName):
  """
  Given a model params dictionary, create a CLA Model. Automatically enables
  inference for predicted field.
  :param modelParams: Model params dict
  :return: OPF Model object
  """
  # Get the new parameters from the csv file
  ImportParams = getNewParams(InputName)
  params = getScalarMetricWithTimeOfDayAnomalyParams(
          metricData=ImportParams[1],
          tmImplementation="cpp",
          minVal=ImportParams[2],
          maxVal=ImportParams[3])
  params['modelConfig']['modelParams']['clEnable'] = True
  model = ModelFactory.create(modelConfig=params["modelConfig"])
  model.enableLearning()  
  model.enableInference(params["inferenceArgs"])
  return model





def runIoThroughNupic(inputData, model, InputName, plot):
  """
  Handles looping over the input data and passing each row into the given model
  object, as well as extracting the result object and passing it into an output
  handler.
  :param inputData: file path to input data CSV
  :param model: OPF Model object
  :param InputName: Gym name, used for output handler naming
  :param plot: Whether to use matplotlib or not. If false, uses file output.
  """
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  if plot:
    output = nupic_anomaly_output.NuPICPlotOutput(InputName)
  else:
    output = nupic_anomaly_output.NuPICFileOutput(InputName)

  counter = 0
  for row in csvReader:
    counter += 1
    if (counter % 100 == 0):
      print "Read %i lines..." % counter
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    PredFldNm = float(row[1])
    result = model.run({
      "c0": timestamp,
      "c1": PredFldNm 
    })


    if plot:
      result = shifter.shift(result)

    prediction = result.inferences["multiStepBestPredictions"][1]
    anomalyScore = result.inferences["anomalyScore"]
    output.write(timestamp, PredFldNm, prediction, anomalyScore)

  inputFile.close()
  output.close()



def runModel(InputName, plot=False):
  """
  Assumes the gynName corresponds to both a like-named model_params file in the
  model_params directory, and that the data exists in a like-named CSV file in
  the current directory.
  :param InputName: Important for finding model params and input CSV file
  :param plot: Plot in matplotlib? Don't use this unless matplotlib is
  installed.
  """
  print "Creating model from %s..." % InputName 
  model = createModel(InputName)
  inputData = "%s/%s.csv" % (DATA_DIR, InputName.replace(" ", "_"))
  runIoThroughNupic(inputData, model, InputName, plot)



if __name__ == "__main__":
  print DESCRIPTION
  plot = False
  args = sys.argv[1:]  
  if "--plot" in args[0]:
    plot = True
  for x in args:
      if '--plot' not in x:
          INPUT_FILE = x[:-4]   
  try: 
      INPUT_FILE
  except NameError:
      raise ValueError('Need to enter the name of a csv file as an argument')
  runModel(INPUT_FILE, plot=plot)