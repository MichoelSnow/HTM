# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:19:23 2017

@author: BJ
"""
from __future__ import absolute_import, division, print_function
import numpy
numpy.set_printoptions(threshold=numpy.nan)
from nupic.encoders import ScalarEncoder

# Scalar encoders
# n is number of bits
# w is the number of on bits
# minval and maxval is the range the bits represent
enc = ScalarEncoder(n=22, w=3, minval=2.5, maxval=97.5, clipInput=True, forced=True)
enc = ScalarEncoder(n=22, w=3, minval=0, maxval=100, clipInput=True, forced=True)
[print(enc.encode(i)) for i in xrange(1,10)]
print("3 =", enc.encode(10200))


enc = ScalarEncoder(n=14, w=3, minval=1, maxval=8, clipInput=True, forced=True, periodic=True)

enc.encode(1.5)
