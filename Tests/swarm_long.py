# -*- coding: utf-8 -*-
"""
Created on Thu May 04 21:04:19 2017

@author: BJ
"""
#import collections
#import imp
#import csv
#from datetime import datetime, timedelta
#import cPickle as pickle
#import time
#import subprocess
import os

from nupic.swarming.hypersearch import object_json as json

#import nupic.database.ClientJobsDAO as cjdao
#from nupic.swarming import HypersearchWorker
#from nupic.swarming.HypersearchV2 import HypersearchV2
from nupic.swarming.exp_generator.ExpGenerator import expGenerator
#from nupic.swarming.utils import *


DEFAULT_OPTIONS = {"overwrite": False,
                  "expDescJsonPath": None,
                  "expDescConfig": None,
                  "permutationsScriptPath": None,
                  "outputLabel": "swarm_out",
                  "outDir": None,
                  "permWorkDir": None,
                  "action": "run",
                  "searchMethod": "v2",
                  "timeout": None,
                  "exports": None,
                  "useTerminators": False,
                  "maxWorkers": 2,
                  "replaceReport": False,
                  "maxPermutations": None,
                  "genTopNDescriptions": 1}


def runWithConfig(swarmConfig, options,
                  outDir=None, outputLabel="default",
                  permWorkDir=None, verbosity=1):
  """
  Starts a swarm, given an dictionary configuration.
  @param swarmConfig {dict} A complete [swarm description](https://github.com/numenta/nupic/wiki/Running-Swarms#the-swarm-description) object.
  @param outDir {string} Optional path to write swarm details (defaults to
                         current working directory).
  @param outputLabel {string} Optional label for output (defaults to "default").
  @param permWorkDir {string} Optional location of working directory (defaults
                              to current working directory).
  @param verbosity {int} Optional (1,2,3) increasing verbosity of output.

  @returns {object} Model parameters
  """
  global g_currentVerbosityLevel
  g_currentVerbosityLevel = verbosity

  # Generate the description and permutations.py files in the same directory
  #  for reference.
  if outDir is None:
    outDir = os.getcwd()
  if permWorkDir is None:
    permWorkDir = os.getcwd()
    
    

#  _checkOverwrite(options, outDir)
  overwrite = options["overwrite"]
  if not overwrite:
    for name in ("description.py", "permutations.py"):
      if os.path.exists(os.path.join(outDir, name)):
        raise RuntimeError("The %s file already exists and will be "
                           "overwritten by this tool. If it is OK to overwrite "
                           "this file, use the --overwrite option." % \
                           os.path.join(outDir, "description.py"))
  # The overwrite option has already been used, so should be removed from the
  # config at this point.
  del options["overwrite"]
#  
  

#  _generateExpFilesFromSwarmDescription(swarmConfig, outDir)
  # The expGenerator expects the JSON without newlines for an unknown reason.
  expDescConfig = json.dumps(swarmConfig)
  expDescConfig = expDescConfig.splitlines()
  expDescConfig = "".join(expDescConfig)

  expGenerator([
    "--description=%s" % (expDescConfig),
    "--outDir=%s" % (outDir)])
#    
    
  
  

  options["expDescConfig"] = swarmConfig
  options["outputLabel"] = outputLabel
  options["outDir"] = outDir
  options["permWorkDir"] = permWorkDir

#  runOptions = _injectDefaultOptions(options)
#  return dict(DEFAULT_OPTIONS, **options)
  runOptions = dict(DEFAULT_OPTIONS, **options)
#  
  
  
#  _validateOptions(runOptions)
#  def _validateOptions(options):
  if "expDescJsonPath" not in runOptions \
    and "expDescConfig" not in runOptions \
    and "permutationsScriptPath" not in runOptions:
    raise Exception("Options must contain one of the following: "
                    "expDescJsonPath, expDescConfig, or "
                    "permutationsScriptPath.")
#


#  return _runAction(runOptions)
#  def _runAction(runOptions):
  if not os.path.exists(runOptions["outDir"]):
    os.makedirs(runOptions["outDir"])
  if not os.path.exists(runOptions["permWorkDir"]):
    os.makedirs(runOptions["permWorkDir"])

  action = runOptions["action"]
  # Print Nupic HyperSearch results from the current or last run
  if action == "report":
    returnValue = _HyperSearchRunner.generateReport(
        options=runOptions,
        replaceReport=runOptions["replaceReport"],
        hyperSearchJob=None,
        metricsKeys=None)
  # Run HyperSearch
  elif action in ("run", "dryRun", "pickup"):
    returnValue = _runHyperSearch(runOptions)
#    def _runHyperSearch(runOptions):
      global gCurrentSearch
      # Run HyperSearch
      startTime = time.time()
      search = _HyperSearchRunner(runOptions)
      # Save in global for the signal handler.
      gCurrentSearch = search
      if runOptions["action"] in ("run", "dryRun"):
        search.runNewSearch()
      else:
        search.pickupSearch()
    
      # Generate reports
      # Print results and generate report csv file
      modelParams = _HyperSearchRunner.generateReport(
        options=runOptions,
        replaceReport=runOptions["replaceReport"],
        hyperSearchJob=search.peekSearchJob(),
        metricsKeys=search.getDiscoveredMetricsKeys())
      secs = time.time() - startTime
      hours = int(secs) / (60 * 60)
      secs -= hours * (60 * 60)
      minutes = int(secs) / 60
      secs -= minutes * 60
      print "Elapsed time (h:mm:ss): %d:%02d:%02d" % (hours, minutes, int(secs))
      jobID = search.peekSearchJob().getJobID()
      print "Hypersearch ClientJobs job ID: ", jobID

      return modelParams
#



  else:
    raise Exception("Unhandled action: %s" % action)
  return returnValue
#