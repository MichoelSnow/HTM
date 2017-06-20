# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:05:31 2017

@author: msnow1
"""
model = createModel(InputName)
counter = 0
for row in csvReader:
    counter += 1
    if (counter % 300 == 0):
        print "Read %i lines..." % counter
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    PredFld = [float(row[Ct]) for Ct in xrange(1,len(ColNm))]
    ResDict = {ColNm[x] : PredFld[x-1] for x in xrange(1,len(ColNm))}
    ResDict["timestamp"] = timestamp
    result = model.run(ResDict)
    
    result = shifter.shift(result)
#        steps2 = result2.inferences["multiStepBestPredictions"].keys()
#        prediction2 += [result2.inferences["multiStepBestPredictions"][steps2[0]]]
    
    steps = result.inferences["multiStepBestPredictions"].keys()
    prediction = result.inferences["multiStepBestPredictions"][steps[0]]
    anomalyScore = result.inferences["anomalyScore"]
#    output.write(timestamp, PredFld[0], prediction, anomalyScore)