# -*- coding: utf-8 -*-
"""
Created on Mon May 01 07:18:53 2017

@author: msnow1
"""

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
# Swarm Description Dictionary:
#
# Define the swarm description parameters
#



SWARM_DESCRIPTION = {
	# The fields to be included in the swarm and the appropriate descriptors
	# Field types and optional descriptors
	# datetime - NONE
	# float - minValue, maxValue
  "includedFields": [
    {
      "fieldName": "timestamp",
      "fieldType": "datetime"
    },
    {
      "fieldName": "Ct",
      "fieldType": "float",
      "maxValue": 6.0,
      "minValue": 0
    },
  ],
  # Name of the csv data file 
  "streamDef": {
    "info": "Ct",
    "version": 1,
    "streams": [
      {
        "info": "Fndng Ct",
        "source": "file://HMdata.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },
	# type of inference - Multistep, NontemporalMultistep, 
		# TemporalMultiStep, TemporalAnomaly
  "inferenceType": "TemporalAnomaly",
  "inferenceArgs": {
	# number of steps in advance to predict
    "predictionSteps": [1], 
	# name of the csv filed to predict
    "predictedField": "Ct"
  },
  # Number of rows to swarm over, -1 assumes all rows
  "iterationCount": 100, 
  # Swarm size tells it how big of aswarm to runs
	# small -> debugging
	# medium -> usually what you want
	# large -> long time but slightly better model params than medium
  "swarmSize": "medium" 
}