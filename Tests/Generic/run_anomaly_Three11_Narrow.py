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
import importlib
import sys
import csv
import datetime
import os
import getpass
os.environ["USER"] = getpass.getuser()

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

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





def createModel(modelParams):
  """
  Given a model params dictionary, create a CLA Model. Automatically enables
  inference for predicted field.
  :param modelParams: Model params dict
  :return: OPF Model object
  """
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "counts"})
  return model



def getModelParamsFromName(InputName):
  """
  Given a gym name, assumes a matching model params python module exists within
  the model_params directory and attempts to import it.
  :param InputName: Gym name, used to guess the model params module name.
  :return: OPF Model params dictionary
  """
  importName = "model_params.%s_model_params" % (
    InputName.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % InputName)
  return importedModelParams



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
    counts = float(row[1])
    result = model.run({
      "timestamp": timestamp,
      "counts": counts 
    })

    if plot:
      result = shifter.shift(result)

    prediction = result.inferences["multiStepBestPredictions"][1]
    anomalyScore = result.inferences["anomalyScore"]
    output.write(timestamp, counts, prediction, anomalyScore)

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
  model = createModel(getModelParamsFromName(InputName))
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