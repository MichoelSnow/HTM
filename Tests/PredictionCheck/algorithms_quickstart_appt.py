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
_INPUT_FILE_PATH = os.path.join(_EXAMPLE_DIR, "data", "appt_htm_1steps.csv")
_PARAMS_PATH = os.path.join(_EXAMPLE_DIR, "params", "model_appt_0steps.yaml")
_FILE_NAME = os.path.basename(os.path.splitext(_INPUT_FILE_PATH)[0])



def runHotgym(numRecords):
  with open(_PARAMS_PATH, "r") as f:
    modelParams = yaml.safe_load(f)["modelParams"]
    enParams = modelParams["sensorParams"]["encoders"]
    spParams = modelParams["spParams"]
    tmParams = modelParams["tmParams"]

  timeOfDayEncoder = DateEncoder(timeOfDay=enParams["timestamp_timeOfDay"]["timeOfDay"])
  weekendEncoder = DateEncoder(weekend=enParams["timestamp_weekend"]["weekend"])
  CtEncoder = RandomDistributedScalarEncoder(enParams["Ct"]["resolution"])
  ZIP_10467Encoder = RandomDistributedScalarEncoder(enParams["ZIP_10467"]["resolution"])
#  ZIP_10462Encoder = RandomDistributedScalarEncoder(enParams["ZIP_10462"]["resolution"])
#  ZIP_10475Encoder = RandomDistributedScalarEncoder(enParams["ZIP_10475"]["resolution"])
#  ZIP_10466Encoder = RandomDistributedScalarEncoder(enParams["ZIP_10466"]["resolution"])
#  ZIP_10469Encoder = RandomDistributedScalarEncoder(enParams["ZIP_10469"]["resolution"])
#  DEPT_11Encoder = RandomDistributedScalarEncoder(enParams["DEPT_11"]["resolution"])
#  DEPT_24Encoder = RandomDistributedScalarEncoder(enParams["DEPT_24"]["resolution"])
#  DEPT_41Encoder = RandomDistributedScalarEncoder(enParams["DEPT_41"]["resolution"])
#  DEPT_34Encoder = RandomDistributedScalarEncoder(enParams["DEPT_34"]["resolution"])
#  DEPT_31Encoder = RandomDistributedScalarEncoder(enParams["DEPT_31"]["resolution"])
#  DEPT_60Encoder = RandomDistributedScalarEncoder(enParams["DEPT_60"]["resolution"])
#  AGE_0_9Encoder = RandomDistributedScalarEncoder(enParams["AGE_0_9"]["resolution"])
#  AGE_10_19Encoder = RandomDistributedScalarEncoder(enParams["AGE_10_19"]["resolution"])
#  AGE_20_29Encoder = RandomDistributedScalarEncoder(enParams["AGE_20_29"]["resolution"])
#  AGE_30_39Encoder = RandomDistributedScalarEncoder(enParams["AGE_30_39"]["resolution"])
#  AGE_40_49Encoder = RandomDistributedScalarEncoder(enParams["AGE_40_49"]["resolution"])
#  AGE_50_59Encoder = RandomDistributedScalarEncoder(enParams["AGE_50_59"]["resolution"])
#  AGE_60_69Encoder = RandomDistributedScalarEncoder(enParams["AGE_60_69"]["resolution"])
#  AGE_70_79Encoder = RandomDistributedScalarEncoder(enParams["AGE_70_79"]["resolution"])
#  AGE_80_89Encoder = RandomDistributedScalarEncoder(enParams["AGE_80_89"]["resolution"])
#  AGE_90_99Encoder = RandomDistributedScalarEncoder(enParams["AGE_90_99"]["resolution"])
#  DIST_1_7Encoder = RandomDistributedScalarEncoder(enParams["DIST_1_7"]["resolution"])
#  DIST_8_14Encoder = RandomDistributedScalarEncoder(enParams["DIST_8_14"]["resolution"])
#  DIST_15_21Encoder = RandomDistributedScalarEncoder(enParams["DIST_15_21"]["resolution"])
#  DIST_22_28Encoder = RandomDistributedScalarEncoder(enParams["DIST_22_28"]["resolution"])
#  DIST_29_35Encoder = RandomDistributedScalarEncoder(enParams["DIST_29_35"]["resolution"])
#  DIST_36_42Encoder = RandomDistributedScalarEncoder(enParams["DIST_36_42"]["resolution"])
#  DIST_43_49Encoder = RandomDistributedScalarEncoder(enParams["DIST_43_49"]["resolution"])
#  DIST_50_56Encoder = RandomDistributedScalarEncoder(enParams["DIST_50_56"]["resolution"])
#  DIST_57_63Encoder = RandomDistributedScalarEncoder(enParams["DIST_57_63"]["resolution"])
#  DIST_64_70Encoder = RandomDistributedScalarEncoder(enParams["DIST_64_70"]["resolution"])
  


  encodingWidth = (timeOfDayEncoder.getWidth()
                   + weekendEncoder.getWidth()
                   + CtEncoder.getWidth()*2)

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
      dateString = datetime.datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S")
      # Convert data value string into float.
      Ct = float(record[1])
      ZIP_10467 = float(record[2])
#      ZIP_10462 = float(record[3])
#      ZIP_10475 = float(record[4])
#      ZIP_10466 = float(record[5])
#      ZIP_10469 = float(record[6])
#      DEPT_11 = float(record[7])
#      DEPT_24 = float(record[8])
#      DEPT_41 = float(record[9])
#      DEPT_34 = float(record[10])
#      DEPT_31 = float(record[11])
#      DEPT_60 = float(record[12])
#      AGE_0_9 = float(record[13])
#      AGE_10_19 = float(record[14])
#      AGE_20_29 = float(record[15])
#      AGE_30_39 = float(record[16])
#      AGE_40_49 = float(record[17])
#      AGE_50_59 = float(record[18])
#      AGE_60_69 = float(record[19])
#      AGE_70_79 = float(record[20])
#      AGE_80_89 = float(record[21])
#      AGE_90_99 = float(record[22])
#      DIST_1_7 = float(record[23])
#      DIST_8_14 = float(record[24])
#      DIST_15_21 = float(record[25])
#      DIST_22_28 = float(record[26])
#      DIST_29_35 = float(record[27])
#      DIST_36_42 = float(record[28])
#      DIST_43_49 = float(record[29])
#      DIST_50_56 = float(record[30])
#      DIST_57_63 = float(record[31])
#      DIST_64_70 = float(record[31])



      # To encode, we need to provide zero-filled numpy arrays for the encoders
      # to populate.
      timeOfDayBits = numpy.zeros(timeOfDayEncoder.getWidth())
      weekendBits = numpy.zeros(weekendEncoder.getWidth())
      CtBits = numpy.zeros(CtEncoder.getWidth())
      ZIP_10467Bits = numpy.zeros(ZIP_10467Encoder.getWidth())
#      ZIP_10462Bits = numpy.zeros(ZIP_10462Encoder.getWidth())
#      ZIP_10475Bits = numpy.zeros(ZIP_10475Encoder.getWidth())
#      ZIP_10466Bits = numpy.zeros(ZIP_10466Encoder.getWidth())
#      ZIP_10469Bits = numpy.zeros(ZIP_10469Encoder.getWidth())
#      DEPT_11Bits = numpy.zeros(DEPT_11Encoder.getWidth())
#      DEPT_24Bits = numpy.zeros(DEPT_24Encoder.getWidth())
#      DEPT_41Bits = numpy.zeros(DEPT_41Encoder.getWidth())
#      DEPT_34Bits = numpy.zeros(DEPT_34Encoder.getWidth())
#      DEPT_31Bits = numpy.zeros(DEPT_31Encoder.getWidth())
#      DEPT_60Bits = numpy.zeros(DEPT_60Encoder.getWidth())
#      AGE_0_9Bits = numpy.zeros(AGE_0_9Encoder.getWidth())
#      AGE_10_19Bits = numpy.zeros(AGE_10_19Encoder.getWidth())
#      AGE_20_29Bits = numpy.zeros(AGE_20_29Encoder.getWidth())
#      AGE_30_39Bits = numpy.zeros(AGE_30_39Encoder.getWidth())
#      AGE_40_49Bits = numpy.zeros(AGE_40_49Encoder.getWidth())
#      AGE_50_59Bits = numpy.zeros(AGE_50_59Encoder.getWidth())
#      AGE_60_69Bits = numpy.zeros(AGE_60_69Encoder.getWidth())
#      AGE_70_79Bits = numpy.zeros(AGE_70_79Encoder.getWidth())
#      AGE_80_89Bits = numpy.zeros(AGE_80_89Encoder.getWidth())
#      AGE_90_99Bits = numpy.zeros(AGE_90_99Encoder.getWidth())
#      DIST_1_7Bits = numpy.zeros(DIST_1_7Encoder.getWidth())
#      DIST_8_14Bits = numpy.zeros(DIST_8_14Encoder.getWidth())
#      DIST_15_21Bits = numpy.zeros(DIST_15_21Encoder.getWidth())
#      DIST_22_28Bits = numpy.zeros(DIST_22_28Encoder.getWidth())
#      DIST_29_35Bits = numpy.zeros(DIST_29_35Encoder.getWidth())
#      DIST_36_42Bits = numpy.zeros(DIST_36_42Encoder.getWidth())
#      DIST_43_49Bits = numpy.zeros(DIST_43_49Encoder.getWidth())
#      DIST_50_56Bits = numpy.zeros(DIST_50_56Encoder.getWidth())
#      DIST_57_63Bits = numpy.zeros(DIST_57_63Encoder.getWidth())
#      DIST_64_70Bits = numpy.zeros(DIST_64_70Encoder.getWidth())


      # Now we call the encoders to create bit representations for each value.
      timeOfDayEncoder.encodeIntoArray(dateString, timeOfDayBits)
      weekendEncoder.encodeIntoArray(dateString, weekendBits)
      CtEncoder.encodeIntoArray(Ct, CtBits)
      ZIP_10467Encoder.encodeIntoArray(ZIP_10467, ZIP_10467Bits)
#      ZIP_10462Encoder.encodeIntoArray(ZIP_10462, ZIP_10462Bits)
#      ZIP_10475Encoder.encodeIntoArray(ZIP_10475, ZIP_10475Bits)
#      ZIP_10466Encoder.encodeIntoArray(ZIP_10466, ZIP_10466Bits)
#      ZIP_10469Encoder.encodeIntoArray(ZIP_10469, ZIP_10469Bits)
#      DEPT_11Encoder.encodeIntoArray(DEPT_11, DEPT_11Bits)
#      DEPT_24Encoder.encodeIntoArray(DEPT_24, DEPT_24Bits)
#      DEPT_41Encoder.encodeIntoArray(DEPT_41, DEPT_41Bits)
#      DEPT_34Encoder.encodeIntoArray(DEPT_34, DEPT_34Bits)
#      DEPT_31Encoder.encodeIntoArray(DEPT_31, DEPT_31Bits)
#      DEPT_60Encoder.encodeIntoArray(DEPT_60, DEPT_60Bits)
#      AGE_0_9Encoder.encodeIntoArray(AGE_0_9, AGE_0_9Bits)
#      AGE_10_19Encoder.encodeIntoArray(AGE_10_19, AGE_10_19Bits)
#      AGE_20_29Encoder.encodeIntoArray(AGE_20_29, AGE_20_29Bits)
#      AGE_30_39Encoder.encodeIntoArray(AGE_30_39, AGE_30_39Bits)
#      AGE_40_49Encoder.encodeIntoArray(AGE_40_49, AGE_40_49Bits)
#      AGE_50_59Encoder.encodeIntoArray(AGE_50_59, AGE_50_59Bits)
#      AGE_60_69Encoder.encodeIntoArray(AGE_60_69, AGE_60_69Bits)
#      AGE_70_79Encoder.encodeIntoArray(AGE_70_79, AGE_70_79Bits)
#      AGE_80_89Encoder.encodeIntoArray(AGE_80_89, AGE_80_89Bits)
#      AGE_90_99Encoder.encodeIntoArray(AGE_90_99, AGE_90_99Bits)
#      DIST_1_7Encoder.encodeIntoArray(DIST_1_7, DIST_1_7Bits)
#      DIST_8_14Encoder.encodeIntoArray(DIST_8_14, DIST_8_14Bits)
#      DIST_15_21Encoder.encodeIntoArray(DIST_15_21, DIST_15_21Bits)
#      DIST_22_28Encoder.encodeIntoArray(DIST_22_28, DIST_22_28Bits)
#      DIST_29_35Encoder.encodeIntoArray(DIST_29_35, DIST_29_35Bits)
#      DIST_36_42Encoder.encodeIntoArray(DIST_36_42, DIST_36_42Bits)
#      DIST_43_49Encoder.encodeIntoArray(DIST_43_49, DIST_43_49Bits)
#      DIST_50_56Encoder.encodeIntoArray(DIST_50_56, DIST_50_56Bits)
#      DIST_57_63Encoder.encodeIntoArray(DIST_57_63, DIST_57_63Bits)
#      DIST_64_70Encoder.encodeIntoArray(DIST_64_70, DIST_64_70Bits)
      # Concatenate all these encodings into one large encoding for Spatial
      # Pooling.
      encoding = numpy.concatenate(
        [timeOfDayBits, weekendBits, CtBits,
         ZIP_10467Bits])
#      encoding = numpy.concatenate(
#        [timeOfDayBits, weekendBits, CtBits,
#         ZIP_10467Bits, ZIP_10462Bits, ZIP_10475Bits, ZIP_10466Bits, ZIP_10469Bits,
#         DEPT_11Bits, DEPT_24Bits, DEPT_41Bits, DEPT_34Bits, DEPT_31Bits,
#         DEPT_60Bits, AGE_0_9Bits, AGE_10_19Bits, AGE_20_29Bits, AGE_30_39Bits,
#         AGE_40_49Bits, AGE_50_59Bits, AGE_60_69Bits, AGE_70_79Bits, AGE_80_89Bits,
#         AGE_90_99Bits, DIST_1_7Bits, DIST_8_14Bits, DIST_15_21Bits, DIST_22_28Bits,
#         DIST_29_35Bits, DIST_36_42Bits, DIST_43_49Bits, DIST_50_56Bits, DIST_57_63Bits,
#         DIST_64_70Bits])    

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
      bucketIdx = CtEncoder.getBucketIndices(Ct)[0]

      # Run classifier to translate active cells back to scalar value.
      classifierResult = classifier.compute(
        recordNum=count,
        patternNZ=activeCells,
        classification={
          "bucketIdx": bucketIdx,
          "actValue": Ct
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
      results.append([record[0], Ct, oneStep, oneStepConfidence * 100])
      output.write(record[0], Ct, oneStep, oneStepConfidence * 100)
    
    output.close()
    return results

# %%
if __name__ == "__main__":
  runHotgym(_NUM_RECORDS)