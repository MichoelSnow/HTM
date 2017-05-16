# -*- coding: utf-8 -*-
"""
Created on Fri May 05 10:50:38 2017

@author: msnow1
"""

from nupic.research.spatial_pooler import SpatialPooler


def SP(**kwargs):
    """
    @param inputDimensions:
        Comma separated list of the input encoder dimensions, i.e., 
        (height, width, depth, ...).  Ex: a one dimensional vector of length 
        100 is represented by (100), a 3 by 20 array is represented by (3,20)
    
    @param columnDimensions:
        Comma separated list of the pooler dimensions, i.e., 
        (height, width, depth, ...).  Ex: a one dimensional vector of length 
        100 is represented by (100), a 3 by 20 array is represented by (3,20)
    
    @param potentialRadius:        
        The extent of the input to which each colum can potentially connect to.
        This can be though of as the input bits which the SP can see, or its
        receptive field.  Scalar input which defines a square or hypersquare 
        area with sides of length 2 * potentialRadius + 1.  
    
    @param potentialPct:
        Scalar between 0 and 1 which represents the percent of inputs, within
        a column's potentialRadius, that the column can be connected to.  If
        set to 1, the column will possibly be connected to every input within 
        its potentialRadius
    
    @param globalInhibition:
        If True, then during ihibition the winning columns are those columns
        which are the most active colums within the entire region.  Otherwise,
        the winning columns are slected with respect to the local neighborhoods,
        think of this like a receptive field.  Using global inhibition boosts
        performace x60.
        
    @param localAreaDensity: ?? Not exactly sure what this does
        The desired density of active columns within a local inhibition area
        (the size of which is set by the internally calculated inhibitionRadius,
        which is in turn determined from the average size of the connected
        potential pools of all columns). The inhibition logic will insure that
        at most N columns remain ON within a local inhibition area, where
        N = localAreaDensity * (total number of columns in inhibition area).
    
    @param numActiveColumnsPerInhArea: 
        This specifies the number of winning columns based on the number of 
        connected synapses matching the input vector per inhibition area.  For 
        example if there was global inhibition and numActiveColumnsPerInhArea 
        was set to 10, then the 10 columns with the most number of connected 
        synpases matching the input would be the active columns. In other words
        active columns are the columns with the top X overlap scores. This is 
        an alternate way to control the density of the active columns. If
        numActiveColumnsPerInhArea is specified then localAreaDensity must be
        less than 0, and vice versa.  When using this method, as columns learn 
        and grow their effective receptive fields, the inhibitionRadius will 
        grow, and hence the net density of the active columns will *decrease*. 
        This is in contrast to the localAreaDensity method, which keeps the density of active columns
         the same regardless of the size of their receptive fields.
    
    @param stimulusThreshold:
        Scalar value specifying the minimum number of ON synapses required for
        a column to be ON. Used to prevent input noise from activating a column
        Default is 0       
    
    @param synPermInactiveDec:
        Percent by which an inactive synapse is decremented in each round. An
        inactive synapse is a bit in the input vector connected to an active, 
        aka winning, column but whose bit does not overlap with an ON bit in 
        input vector. Default is 0.008
    
    @param synPermActiveInc:
        Percent by which an active synapse is incremented in each round. An
        active synapse is a bit in the input vector connected to an active, 
        aka winning, column, whose bit overlaps with an ON bit in input vector. 
        Default value is 0.05
    
    @param synPermConnected:
        Syanpse permanence connection threshold above which a synapse is 
        considered a connected synapse.  The SP will try to give a normal 
        distribution of permanence values around this threshold, so that there
        are a lot of synapses whcih are primed to become connected or 
        discoennected. Default is 0.1
    
    @param minPctOverlapDutyCycle:
        Value between 0 and 1.0 which sets the floor on the freqeuncy with 
        which a column has at least stimulusThreshold active inputs.  
        Periodically, based on dutyCyclePeriod, each column looks at the 
        overlap duty cycle of all other columns within its inhibition radius 
        and sets its own minimal acceptable duty cycle to
        minPctDutyCycleBeforeInh * max(other columns' duty cycles)
        On each iteration, if a column's overlap duty cycle is below this value,
        its permanence values will be bosted by synPermActiveInc. Default 
        is 0.001
        
    @param dutyCyclePeriod:
        The period used to calculate duty cycles, where higher values mean a 
        it takes a column longer to repond to changes in boostStrength or 
        stimulusThreshold. Default is 1000
        
    @oaram boostStrength:
        Float >= 0.0 which controls the strength of boosting.  A value of 0, 
        means no boosting.  Boosting encurages columns to have similar 
        activeDutyCycles as their nieghbors, leading to more efficient column 
        use.  However, too much boosting may also lead to SP output instability
    
    @param seed:
        Seed for the pseudo-random number generator. Default is -1
    
    @param wrapAround:
        Determines if inputs at the begnning and end of an input dimension
        should be considered neighbors when mapping columns to inputs.  Default
        is True
        
        
    
    """
    return SpatialPooler(**kwargs)
    
    
    
    
    
    
    
    
    