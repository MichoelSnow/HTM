# -*- coding: utf-8 -*-
"""
Created on Mon May 22 08:32:26 2017

@author: msnow1
"""

# Use dir(ObjectNm) to see all attributes of the object ObjectNm
import os
import importlib
import getpass
import datetime
import csv
os.environ["USER"] = getpass.getuser()


import nupic_anomaly_output

#from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.clamodel import CLAModel
from nupic.frameworks.opf.two_gram_model import TwoGramModel
from nupic.frameworks.opf.previousvaluemodel import PreviousValueModel
from nupic.data.inference_shifter import InferenceShifter


os.chdir('E:\\MyDocuments\\GitHub\\HTM\\Tests\\Generic\\')
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
model.enableInference({"predictedField": "EntriesDif"})

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
for row in csvReader:
    counter += 1
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    EntriesDif = float(row[1])
    result = model.run({"timestamp": timestamp,"EntriesDif": EntriesDif})
    prediction = result.inferences["multiStepBestPredictions"][1]
    anomalyScore = result.inferences["anomalyScore"]
    break
    
# %%






runIoThroughNupic(inputData, model, InputName, plot)