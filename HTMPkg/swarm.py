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
Groups together the code dealing with swarming.
"""
import os
import getpass
import glob
import sys
# Sets the current user as the environment variable USER 
os.environ["USER"] = getpass.getuser()
# pretty printing for the model_params file
import pprint
from multiprocessing import cpu_count

# add logging to output errors to stdout
import logging
logging.basicConfig()

# This is the main function which runs the swarm
# from HTMPkg import permutations_runner
from nupic.swarming import permutations_runner
# imports the parameter variable from swarm_description
from swarm_description import SWARM_DESCRIPTION

# Name of the csv file which contains the data to swarm over
try:
    INPUT_FILE
except NameError:
    # If no INPUT_FILE is assigned when swarm is called this assumes that 
    # there is only one csv file in the current directory and uses it
    INPUT_FILE = ''.join(glob.glob('*.csv'))

DESCRIPTION = (
  "This script runs a swarm on the input data and\n"
  "creates a model parameters file in the `model_params` directory containing\n"
  "the best model found by the swarm. Dumps a bunch of crud to stdout because\n"
  "that is just what swarming does at this point. You really don't need to\n"
  "pay any attention to it.\n"
  )


# Prints out the modelParams variable prettily 
def modelParamsToString(modelParams):
  pp = pprint.PrettyPrinter(indent=2)
  return pp.pformat(modelParams)


# Create a folder named model_params and places the swarmed paramters inside
def writeModelParamsToFile(modelParams, name):
  cleanName = name.replace(" ", "_").replace("-", "_")
  paramsName = "%s_model_params.py" % cleanName
  outDir = os.path.join(os.getcwd(), 'model_params')
  if not os.path.isdir(outDir):
    os.mkdir(outDir)
  # Create an __init__.py so the params are recognized.
  initPath = os.path.join(outDir, '__init__.py')
  open(initPath, 'a').close()
  outPath = os.path.join(os.getcwd(), 'model_params', paramsName)
  with open(outPath, "wb") as outFile:
    modelParamsString = modelParamsToString(modelParams)
    outFile.write("MODEL_PARAMS = \\\n%s" % modelParamsString)
  return outPath


# Runs the swarm
def swarmForBestModelParams(swarmConfig, name, maxWorkers=cpu_count()):
  outputLabel = name
  permWorkDir = os.path.abspath('swarm')
  if not os.path.exists(permWorkDir):
    os.mkdir(permWorkDir)
  modelParams = permutations_runner.runWithConfig(
    swarmConfig,
    {"maxWorkers": maxWorkers, "overwrite": True},
    outputLabel=outputLabel,
    outDir=permWorkDir,
    permWorkDir=permWorkDir,
    verbosity=0
  )
  modelParamsFile = writeModelParamsToFile(modelParams, name)
  return modelParamsFile



def printSwarmSizeWarning(size):
  if size is "small":
    print "= THIS IS A DEBUG SWARM. DON'T EXPECT YOUR MODEL RESULTS TO BE GOOD."
  elif size is "medium":
    print "= Medium swarm. Sit back and relax, this could take awhile."
  else:
    print "= LARGE SWARM! Might as well load up the Star Wars Trilogy."



def swarm(filePath):
  name = os.path.splitext(os.path.basename(filePath))[0]
  print "================================================="
  print "= Swarming on %s data..." % name
  printSwarmSizeWarning(SWARM_DESCRIPTION["swarmSize"])
  print "================================================="
  modelParams = swarmForBestModelParams(SWARM_DESCRIPTION, name)
  print "\nWrote the following model param files:"
  print "\t%s" % modelParams



if __name__ == "__main__":
  print DESCRIPTION
  args = sys.argv[1:]
  INPUT_FILE = args[0] 
  swarm(INPUT_FILE)