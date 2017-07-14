# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 08:56:32 2017

@author: msnow1
"""

from nupic.algorithms.spatial_pooler import SpatialPooler
import numpy as np


class spatial_pooler(object):
    
    def __init__(self,encoding):
        self.encoding = encoding
        self.sp = self.create_sp()
        self.sp_output = self.sp_compute(self.sp,self.encoding)
        
    def create_sp(self):
        sp = SpatialPooler(
          # How large the input encoding will be.
          inputDimensions=(len(self.encoding[0])),
          # How many mini-columns will be in the Spatial Pooler.
          columnDimensions=(2048),
          # What percent of the columns's receptive field is 
          # available for potential synapses?
          potentialPct=0.85,
          # This means that the input space has no topology.
          globalInhibition=True,
          localAreaDensity=-1.0,
          # Roughly 2%, giving that there is only one inhibition area because 
          # we have turned on globalInhibition (40 / 2048 = 0.0195)
          numActiveColumnsPerInhArea=40.0,
          # How quickly synapses grow and degrade.
          synPermInactiveDec=0.005,
          synPermActiveInc=0.04,
          synPermConnected=0.1,
          # boostStrength controls the strength of boosting. Boosting 
          # encourages efficient usage of SP columns.
          boostStrength=3.0,
          # Random number generator seed.
          seed=1956,
          # Determines if inputs at the beginning and end of an input dimension 
          # should be considered neighbors when mapping columns to inputs.
          wrapAround=False)        
        return sp
        
    def sp_compute(self,sp,encoding):
        # Execute Spatial Pooling algorithm over input space.
        sp_output = []
        for i in encoding:
            # Create an array to represent active columns, all initially zero. This
            # will be populated by the compute method below. It must have the same
            # dimensions as the Spatial Pooler.
            activeColumns = np.zeros(2048)
            sp.compute(i, True, activeColumns)
            activeColumnIndices = np.nonzero(activeColumns)[0]
            sp_output += [activeColumnIndices]
        return sp_output
    
    def output_sp(self):
        return self.sp_output
        


