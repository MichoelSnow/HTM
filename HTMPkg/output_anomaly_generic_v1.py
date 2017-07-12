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
Provides two classes with the same signature for writing data out of NuPIC
models.
(This is a component of the One Hot Gym Anomaly Tutorial.)
"""
import csv
from abc import ABCMeta, abstractmethod
from nupic.algorithms import anomaly_likelihood


class NuPICOutput(object):

  __metaclass__ = ABCMeta


  def __init__(self, name):
    self.name = name


  @abstractmethod
  def write(self, timestamp, value, predicted, anomalyScore):
    pass


  @abstractmethod
  def close(self):
    pass




class NuPICFileOutput(NuPICOutput):


  def __init__(self, *args, **kwargs):
    super(NuPICFileOutput, self).__init__(*args, **kwargs)
    self.outputFiles = []
    self.outputWriters = []
    self.lineCount = 0
    headerRow = ['timestamp', 'Ct','prediction', 'anomalyScore']
    outputFileName = "%s_out.csv" % self.name
    print "Preparing to output %s data to %s" % (self.name, outputFileName)
    self.outputFile = open(outputFileName, "w")
    self.outputWriter = csv.writer(self.outputFile)
    self.outputWriter.writerow(headerRow)




  def write(self, timestamp, value, predicted, anomalyScore):
#    if timestamp is not None:
#      try:
#          anomalyLikelihood = self.anomalyLikelihoodHelper.anomalyProbability(
#            value, anomalyScore, timestamp
#          )
#      except:
#          print(value)
#          print(anomalyScore)
#          print(timestamp)
      outputRow = [timestamp, value, predicted, anomalyScore]
      self.outputWriter.writerow(outputRow)
      self.lineCount += 1



  def close(self):
    self.outputFile.close()
    print "Done. Wrote %i data lines to %s." % (self.lineCount, self.name)





NuPICOutput.register(NuPICFileOutput)
