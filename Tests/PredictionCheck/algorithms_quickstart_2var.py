# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:40:15 2017

@author: msnow1
"""


import csv
import datetime
import numpy
import os
import yaml


from nupic.algorithms.sdr_classifier_factory import SDRClassifierFactory
from nupic.algorithms.spatial_pooler import SpatialPooler
from nupic.algorithms.temporal_memory import TemporalMemory
from nupic.encoders.date import DateEncoder
from nupic.encoders.random_distributed_scalar import \
  RandomDistributedScalarEncoder
from HTMPkg import output_anomaly_generic_v1

import getpass
os.environ["USER"] = getpass.getuser()

__file__ = 'E:\\MyDocuments\\GitHub\\HTM\\Tests\\PredictionCheck\\data'
_NUM_RECORDS = 3000
_EXAMPLE_DIR = os.path.dirname(os.path.abspath(__file__))
#_INPUT_FILE_PATH = os.path.join(_EXAMPLE_DIR, os.pardir, "data", "gymdata.csv")
#_PARAMS_PATH = os.path.join(_EXAMPLE_DIR, os.pardir, "params", "model.yaml")
_INPUT_FILE_PATH = os.path.join(_EXAMPLE_DIR, "data", "pred_htm.csv")
_PARAMS_PATH = os.path.join(_EXAMPLE_DIR, "params", "model_2var.yaml")
_FILE_NAME = os.path.basename(os.path.splitext(_INPUT_FILE_PATH)[0])



def runHotgym(numRecords):
  with open(_PARAMS_PATH, "r") as f:
    modelParams = yaml.safe_load(f)["modelParams"]
    enParams = modelParams["sensorParams"]["encoders"]
    spParams = modelParams["spParams"]
    tmParams = modelParams["tmParams"]

  timeOfDayEncoder = DateEncoder(
    timeOfDay=enParams["timestamp_timeOfDay"]["timeOfDay"])
  weekendEncoder = DateEncoder(
    weekend=enParams["timestamp_weekend"]["weekend"])
  scalarEncoder = RandomDistributedScalarEncoder(
    enParams["consumption"]["resolution"])
  scalarEncoder2 = RandomDistributedScalarEncoder(
    enParams["consumption2"]["resolution"])

  encodingWidth = (timeOfDayEncoder.getWidth()
                   + weekendEncoder.getWidth()
                   + scalarEncoder.getWidth()
                   + scalarEncoder2.getWidth())

  sp = SpatialPooler(
    inputDimensions=(encodingWidth,),
    columnDimensions=(spParams["columnCount"],),
    potentialPct=spParams["potentialPct"],
    potentialRadius=encodingWidth,
    globalInhibition=spParams["globalInhibition"],
    localAreaDensity=spParams["localAreaDensity"],
    numActiveColumnsPerInhArea=spParams["numActiveColumnsPerInhArea"],
    synPermInactiveDec=spParams["synPermInactiveDec"],
    synPermActiveInc=spParams["synPermActiveInc"],
    synPermConnected=spParams["synPermConnected"],
    boostStrength=spParams["boostStrength"],
    seed=spParams["seed"],
    wrapAround=True
  )

  tm = TemporalMemory(
    columnDimensions=(tmParams["columnCount"],),
    cellsPerColumn=tmParams["cellsPerColumn"],
    activationThreshold=tmParams["activationThreshold"],
    initialPermanence=tmParams["initialPerm"],
    connectedPermanence=spParams["synPermConnected"],
    minThreshold=tmParams["minThreshold"],
    maxNewSynapseCount=tmParams["newSynapseCount"],
    permanenceIncrement=tmParams["permanenceInc"],
    permanenceDecrement=tmParams["permanenceDec"],
    predictedSegmentDecrement=0.0,
    maxSegmentsPerCell=tmParams["maxSegmentsPerCell"],
    maxSynapsesPerSegment=tmParams["maxSynapsesPerSegment"],
    seed=tmParams["seed"]
  )

  classifier = SDRClassifierFactory.create()
  results = []
  with open(_INPUT_FILE_PATH, "r") as fin:
    reader = csv.reader(fin)
    headers = reader.next()
    reader.next()
    reader.next()
    
    output = output_anomaly_generic_v1.NuPICFileOutput(_FILE_NAME)
    
    for count, record in enumerate(reader):

      if count >= numRecords: break

      # Convert data string into Python date object.
      dateString = datetime.datetime.strptime(record[0], "%m/%d/%y %H:%M")
      # Convert data value string into float.
      prediction = float(record[1])
      prediction2 = float(record[2])

      # To encode, we need to provide zero-filled numpy arrays for the encoders
      # to populate.
      timeOfDayBits = numpy.zeros(timeOfDayEncoder.getWidth())
      weekendBits = numpy.zeros(weekendEncoder.getWidth())
      consumptionBits = numpy.zeros(scalarEncoder.getWidth())
      consumptionBits2 = numpy.zeros(scalarEncoder2.getWidth())

      # Now we call the encoders to create bit representations for each value.
      timeOfDayEncoder.encodeIntoArray(dateString, timeOfDayBits)
      weekendEncoder.encodeIntoArray(dateString, weekendBits)
      scalarEncoder.encodeIntoArray(prediction, consumptionBits)
      scalarEncoder2.encodeIntoArray(prediction2, consumptionBits2)

      # Concatenate all these encodings into one large encoding for Spatial
      # Pooling.
      encoding = numpy.concatenate(
        [timeOfDayBits, weekendBits, consumptionBits, consumptionBits2]
      )

      # Create an array to represent active columns, all initially zero. This
      # will be populated by the compute method below. It must have the same
      # dimensions as the Spatial Pooler.
      activeColumns = numpy.zeros(spParams["columnCount"])

      # Execute Spatial Pooling algorithm over input space.
      sp.compute(encoding, True, activeColumns)
      activeColumnIndices = numpy.nonzero(activeColumns)[0]

      # Execute Temporal Memory algorithm over active mini-columns.
      tm.compute(activeColumnIndices, learn=True)

      activeCells = tm.getActiveCells()

      # Get the bucket info for this input value for classification.
      bucketIdx = scalarEncoder.getBucketIndices(prediction)[0]

      # Run classifier to translate active cells back to scalar value.
      classifierResult = classifier.compute(
        recordNum=count,
        patternNZ=activeCells,
        classification={
          "bucketIdx": bucketIdx,
          "actValue": prediction
        },
        learn=True,
        infer=True
      )

      # Print the best prediction for 1 step out.
      oneStepConfidence, oneStep = sorted(
        zip(classifierResult[1], classifierResult["actualValues"]),
        reverse=True
      )[0]
      # print("1-step: {:16} ({:4.4}%)".format(oneStep, oneStepConfidence * 100))
#      results.append([oneStep, oneStepConfidence * 100, None, None])
      results.append([record[0], prediction, oneStep, oneStepConfidence * 100])
      output.write(record[0], prediction, oneStep, oneStepConfidence * 100)
    
    output.close()
    return results

# %%
if __name__ == "__main__":
  runHotgym(_NUM_RECORDS)