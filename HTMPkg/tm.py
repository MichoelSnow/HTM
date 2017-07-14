# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 13:48:23 2017

@author: msnow1
"""

from nupic.algorithms.temporal_memory import TemporalMemory


class temporal_memory(object):
    
    def __init__(self,sp):
        self.sp = sp
        self.tm = self.create_tm()
        self.tm_output = self.tm_compute(self.tm,self.sp_output)
        
    def create_tm(self):
        tm = TemporalMemory(
          # Must be the same dimensions as the SP
          columnDimensions=(2048, ),
          # How many cells in each mini-column.
          cellsPerColumn=32,
          # A segment is active if it has >= activationThreshold connected synapses
          # that are active due to infActiveState
          activationThreshold=16,
          initialPermanence=0.21,
          connectedPermanence=0.5,
          # Minimum number of active synapses for a segment to be considered during
          # search for the best-matching segments.
          minThreshold=12,
          # The max number of synapses added to a segment during learning
          maxNewSynapseCount=20,
          permanenceIncrement=0.1,
          permanenceDecrement=0.1,
          predictedSegmentDecrement=0.0,
          maxSegmentsPerCell=128,
          maxSynapsesPerSegment=32,
          seed=1960)        
        return tm
        
    def tm_compute(self,tm,sp):
        tm_output = []
        for i in sp:
            # Execute Temporal Memory algorithm over active mini-columns.
            tm.compute(i, learn=True)
            activeCells = tm.getActiveCells()
            tm_output += [activeCells]
        return tm_output
    
    def output_tm(self):
        return self.tm_output
    
    




        
        
        