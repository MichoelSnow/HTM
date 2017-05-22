# -*- coding: utf-8 -*-
"""
Created on Mon May 22 08:32:26 2017

@author: msnow1
"""

# Use dir(ObjectNm) to see all attributes of the object ObjectNm
import os
import importlib
import collections
import getpass
import datetime
import csv
os.environ["USER"] = getpass.getuser()




#from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.clamodel import CLAModel
from nupic.frameworks.opf.two_gram_model import TwoGramModel
from nupic.frameworks.opf.previousvaluemodel import PreviousValueModel
from nupic.data.inference_shifter import InferenceShifter
from nupic.algorithms import anomaly_likelihood


os.chdir('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Generic\\')

import nupic_anomaly_output

INPUT_FILE = 'Trnstl_14_ST_UNION_SQ'


importName = "model_params.%s_model_params" % (
    INPUT_FILE.replace(" ", "_").replace("-", "_")
  )
ModParams = importlib.import_module(importName).MODEL_PARAMS


modelClass = None
if ModParams['model'] == "CLA":
  modelClass = CLAModel
elif ModParams['model'] == "TwoGram":
  modelClass = TwoGramModel
elif ModParams['model'] == "PreviousValue":
  modelClass = PreviousValueModel

model = modelClass(**ModParams['modelParams'])
model.enableInference({"predictedField": "value"})

# %%

DATA_DIR = "."
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

inputData = "%s/%s.csv" % (DATA_DIR, INPUT_FILE.replace(" ", "_"))
inputFile = open(inputData, "rb")
csvReader = csv.reader(inputFile)
# skip header rows
csvReader.next()
csvReader.next()
csvReader.next()
shifter = InferenceShifter()
output = nupic_anomaly_output.NuPICFileOutput(INPUT_FILE)
# %%
counter = 0
valueOut = []
timestampOut = []
predictionOut = []
anomalyScoreOut = []

claLearningPeriod=None
learningPeriod=288
estimationSamples=100
historicWindowSize=8640
reestimationPeriod=100

iteration = 0
_distribution = None
historicalScores = collections.deque(maxlen=historicWindowSize)

"""
NOTE: Anomaly likelihood scores are reported at a flat 0.5 for
learningPeriod + estimationSamples iterations.

claLearningPeriod and learningPeriod are specifying the same variable,
although claLearningPeriod is a deprecated name for it.

@param learningPeriod (claLearningPeriod: deprecated) - (int) the number of
  iterations required for the algorithm to learn the basic patterns in the
  dataset and for the anomaly score to 'settle down'. The default is based
  on empirical observations but in reality this could be larger for more
  complex domains. The downside if this is too large is that real anomalies
  might get ignored and not flagged.

@param estimationSamples - (int) the number of reasonable anomaly scores
  required for the initial estimate of the Gaussian. The default of 100
  records is reasonable - we just need sufficient samples to get a decent
  estimate for the Gaussian. It's unlikely you will need to tune this since
  the Gaussian is re-estimated every 10 iterations by default.

@param historicWindowSize - (int) size of sliding window of historical
  data points to maintain for periodic reestimation of the Gaussian. Note:
  the default of 8640 is based on a month's worth of history at 5-minute
  intervals.

@param reestimationPeriod - (int) how often we re-estimate the Gaussian
  distribution. The ideal is to re-estimate every iteration but this is a
  performance hit. In general the system is not very sensitive to this
  number as long as it is small relative to the total number of records
  processed.
"""

probationaryPeriod = learningPeriod + estimationSamples

for row in csvReader:
    counter += 1
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    value = float(row[1])
    result = model.run({"timestamp": timestamp,"value": value})
    timestampOut.append(timestamp)
    valueOut.append(value)
    prediction = result.inferences["multiStepBestPredictions"][1]
    anomalyScore = result.inferences["anomalyScore"]
    predictionOut.append(prediction)
    anomalyScoreOut.append(anomalyScore)
    
    dataPoint = (timestamp, value, anomalyScore)
    
    if iteration < probationaryPeriod:
        likelihood = 0.5
    else:
        if ((_distribution is None) or  (iteration % reestimationPeriod == 0)):
            
            numShiftedOut = max(0, iteration - historicalScores.maxlen)
            numSkipRecords = min(iteration, 
                                 max(0, learningPeriod - numShiftedOut))
            
            
            _, _, _distribution = estimateAnomalyLikelihoods(
                    historicalScores, skipRecords=numSkipRecords)
        
        
        likelihoods, _, _distribution = updateAnomalyLikelihoods(
        [dataPoint], _distribution)
        likelihood = 1.0 - likelihoods[0]
    
    
    historicalScores.append(dataPoint)
    iteration += 1
    
    anomalyLikelihoodHelper = anomaly_likelihood.AnomalyLikelihood()
    anomalyLikelihood = anomalyLikelihoodHelper.anomalyProbability(
            value, anomalyScore, timestamp)
    if counter == 10:
        break
    
# %%






runIoThroughNupic(inputData, model, InputName, plot)