# -*- coding: utf-8 -*-
"""
Created on Fri May 05 09:08:38 2017

@author: msnow1
"""

from nupic.encoders.scalar import ScalarEncoder
from nupic.encoders.random_distributed_scalar import RandomDistributedScalarEncoder 
#from nupic.encoders.date import DateEncoder
from nupic.encoders.adaptive_scalar import AdaptiveScalarEncoder
#from nupic.encoders.logenc import LogEncoder
from nupic.encoders.category import CategoryEncoder
from nupic.encoders.coordinate import CoordinateEncoder
from nupic.encoders.delta import DeltaEncoder
from nupic.encoders.geospatial_coordinate import GeospatialCoordinateEncoder
#from nupic.encoders.pass_through_encoder import PassThroughEncoder
from nupic.encoders.scalar_space import ScalarSpaceEncoder
from nupic.encoders.sdr_category import SDRCategoryEncoder
from nupic.encoders.sparse_pass_through import SparsePassThroughEncoder
# multiencoder must be imported last because it imports * from this module!
from nupic.encoders.multi import MultiEncoder
from nupic.encoders.utils import bitsToString

import numpy
numpy.set_printoptions(threshold=numpy.nan)
from datetime import datetime
from pandas.tseries.holiday import USFederalHolidayCalendar as FedHol
import pandas as pd
#import sys
#sys.path.append('E:\\MyDocuments\\GitHub\\HTM\\')

from HTMPkg.date import DateEncoder
# %%

# SCALAR ENCODER
def SE(**kwargs):
    """ 
    SCALAR ENCODER, see definition for more info
    Parameters -- 
    .. warning:: There are three mutually exclusive parameters that determine the 
    overall size of of the output. Exactly one of n, radius, resolution must be 
    set. "0" is a special value that means "not set".
    
    @param w: Number of ON bits which encode a single value, must be odd
    
    @param minval: Minimum value of input signal
    
    @param maxval: Maximum value of the input signal
    
    @param periodic: if true, then input "wraps around" such that the
        input must be strictly less than maxval. Default is False
    
    @param n: Total number of bits in the output must be >= w
    
    @param radius: inputs separated by more than the radius will have
        non-overlapping representations
    
    @param resolution: inputs separated by more than the resolution will have
        different, but possible overlapping,  representations
    
    @param name: Optional string which will become part of the description
    
    @param clipInput: if True, non-periodic inputs < minval or > maxval will be
        clipped to minval and maxval, respectively
        
    @param forced: if True, skip some safety checks.  Default is False
    """
    return ScalarEncoder(**kwargs)

ScalarEncoder(w=11,minval=1,maxval=100,periodic=False,resolution=1,forced=True).encode(100)


ScalarEncoder(w=3,minval=-10,maxval=10,periodic=False,resolution=1,forced=True).encode(8)
ScalarEncoder(w=3,minval=-10,maxval=10,periodic=True,resolution=2,forced=True).encode(9)


# SCALAR ENCODER EXAMPLES
# Encoding the temperature in Farenheit using a single value for every degree
SETmp = SE(w=1,minval=-100,maxval=120,periodic=False,resolution=1,forced=True)
print SETmp.encode(105)

# This is not really that helpful and usually you don't care that much about
# each individual degree, so now encoding the temp so that the representation
# changes only every 5 degrees, also increasing w to 3
SETmp = SE(w=3,minval=-100,maxval=120,periodic=False,resolution=5,forced=True)
print SETmp.encode(1)

# Now let's see what happens if instead of setting the resolution we set the 
# number of bits equal to 50 instead
SETmp = SE(w=3,minval=-100,maxval=120,periodic=False,n=20,forced=True)
print SETmp.encode(-81)
# now the resolution is about 12 degrees

# Now instead of encoding the temperature let's encode the time in terms of 
# a 24 hour period, now we want to have a periodic encoder as 23:50 is very similar
# to 00:15 
SEHr = SE(w=5,minval=0,maxval=24.01,periodic=True,resolution=0.25,forced=True)
print SEHr.encode(0.1)



# RANDOM DISTRIBUTED SCALAR ENCODER
def RDSE(**kwargs):
    """ 
    RANDOM DISTRIBUTED SCALAR ENCODER, see definition for more info
    Parameters --     
    
    @param resolution: inputs separated by more than the resolution will have
        different, but possible overlapping, representations 
    
    @param w: Number of ON bits which encode a single value, must be odd to
        to avoid centering problems
    
    @param n: Total number of bits in the output must be >= w
        
    @param name: Optional string which will become part of the description
    
    @param offset: Floating point offset used to map scalar inputs to bucket
        indices. If set to None, the very first input that is encoded will be 
        used to determine the offset.
    
    @param seed: Seed used by numpy rnadom number generator, if set to -1, the
        generator will be initialized without a fixed seed       
    """
    return RandomDistributedScalarEncoder(**kwargs)

A = RDSE(resolution=3, w=1, n=7)
A.encode(50)
A.encode(3)


# RANDOM DISTRIBUTED SCALAR ENCODER EXAMPLES
# Repetition of our ealier temperature example
RDSETmp = RDSE(resolution=5, w=3, n=20)
print RDSETmp.encode(20)


def DE(**kwargs):
    return DateEncoder(**kwargs)
    """A date encoder encodes a date according to encoding parameters
    specified in its constructor.
    The input to a date encoder is a datetime.datetime object. The output
    is the concatenation of several sub-encodings, each of which encodes
    a different aspect of the date. Which sub-encodings are present, and
    details of those sub-encodings, are specified in the DateEncoder
    constructor.

    Each parameter describes one attribute to encode. By default, the attribute
    is not encoded.

    season (season of the year; units = day):
        (int) width of attribute; default radius = 91.5 days (1 season)
        (tuple)  season[0] = width; season[1] = radius

    dayOfWeek (monday = 0; units = day)
        (int) width of attribute; default radius = 1 day
        (tuple) dayOfWeek[0] = width; dayOfWeek[1] = radius

    weekend (boolean: 0, 1)
        (int) width of attribute

    holiday (boolean: 0, 1)
        (int) width of attribute

    timeOfday (midnight = 0; units = hour)
        (int) width of attribute: default radius = 4 hours
        (tuple) timeOfDay[0] = width; timeOfDay[1] = radius

    customDays TODO: what is it?

    forced (default True) : if True, skip checks for parameters' settings; 
    see encoders/scalar.py for details

    """   
    
DE(weekend=3,season=9,timeOfDay=5).encode(datetime.strptime('04/04/17 12:03', '%m/%d/%y %H:%M'))

ENC = DE(weekend=7,season=11,timeOfDay=7).encode(datetime.strptime('03/04/17 12:00', '%m/%d/%y %H:%M'))
print ENC,len(ENC)


ENC1 = DE(timeOfDay=7).encode(datetime.strptime('03/01/17 12:00', '%m/%d/%y %H:%M'))
ENC2 = DE(weekend=7).encode(datetime.strptime('03/01/17 12:00', '%m/%d/%y %H:%M'))
ENC3 = DE(season=11).encode(datetime.strptime('03/01/17 12:00', '%m/%d/%y %H:%M'))
print ENC1,len(ENC1)
print ENC2,len(ENC2)
print ENC3,len(ENC3)

ENC1 = DE(weekend=7).encode(datetime.strptime('03/04/17 12:00', '%m/%d/%y %H:%M'))
ENC2 = DE(season=11).encode(datetime.strptime('03/04/17 12:00', '%m/%d/%y %H:%M'))
ENC3 = DE(timeOfDay=7).encode(datetime.strptime('03/04/17 12:00', '%m/%d/%y %H:%M'))
print ENC1,len(ENC1)
print ENC2,len(ENC2)
print ENC3,len(ENC3)

ENC1 = DE(timeOfDay=7).encode(datetime.strptime('12/15/17 23:00', '%m/%d/%y %H:%M'))
ENC2 = DE(weekend=7).encode(datetime.strptime('12/15/17 23:00', '%m/%d/%y %H:%M'))
ENC3 = DE(season=11).encode(datetime.strptime('12/15/17 23:00', '%m/%d/%y %H:%M'))
print ENC1,len(ENC1)
print ENC2,len(ENC2)
print ENC3,len(ENC3)



DE(weekend=3).encode(datetime.strptime('02/04/17 12:03', '%m/%d/%y %H:%M'))

ENC = DE(season=3).encode(datetime.strptime('01/01/17 12:03', '%m/%d/%y %H:%M'))
print ENC, len(ENC)

dt1 = datetime.strptime('01/04/16 01:00', '%m/%d/%y %H:%M')
dt2 = datetime.strptime('01/01/17 01:00', '%m/%d/%y %H:%M')

HolRng = FedHol.holidays(FedHol(),start = dt1,end = dt2 + pd.Timedelta('365 days'))
DE(customDays = (3,'mon')).encode(datetime.strptime('06/12/17 12:03', '%m/%d/%y %H:%M'))

dt = pd.to_datetime(datetime.strptime('12/25/17 01:03', '%m/%d/%y %H:%M'))
DE(holiday = 9).encode(pddt)

holtm = FedHol.holidays(FedHol(),start = pddt - pd.Timedelta('100 days'), end= pddt + pd.Timedelta('100 days') )
# %%
pddt = datetime.strptime('12/24/17 23:03', '%m/%d/%y %H:%M')
holtm = FedHol.holidays(FedHol(),start = pddt - pd.Timedelta('2 days'), end= pddt + pd.Timedelta('2 days') )
DateEncoder(holiday = 21).encode(pddt)


