# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 08:56:32 2017

@author: msnow1
"""

from HTMPkg.sdr_encoder import sdr_encoder
from nupic.algorithms.spatial_pooler import SpatialPooler
import numpy as np

file_name = "E:\\MyDocuments\\GitHub\\HTM\\AlgorithmComponents\\Data\\appt_htm_0steps.csv"
encoding = sdr_encoder(file_name).create_encoding()

sp = SpatialPooler(
  # How large the input encoding will be.
  inputDimensions=(len(encoding[0])),
  # How many mini-columns will be in the Spatial Pooler.
  columnDimensions=(2048),
  # What percent of the columns's receptive field is available for potential
  # synapses?
  potentialPct=0.85,
  # This means that the input space has no topology.
  globalInhibition=True,
  localAreaDensity=-1.0,
  # Roughly 2%, giving that there is only one inhibition area because we have
  # turned on globalInhibition (40 / 2048 = 0.0195)
  numActiveColumnsPerInhArea=40.0,
  # How quickly synapses grow and degrade.
  synPermInactiveDec=0.005,
  synPermActiveInc=0.04,
  synPermConnected=0.1,
  # boostStrength controls the strength of boosting. Boosting encourages
  # efficient usage of SP columns.
  boostStrength=3.0,
  # Random number generator seed.
  seed=1956,
  # Determines if inputs at the beginning and end of an input dimension should
  # be considered neighbors when mapping columns to inputs.
  wrapAround=False
)

# Create an array to represent active columns, all initially zero. This
# will be populated by the compute method below. It must have the same
# dimensions as the Spatial Pooler.
activeColumns = np.zeros(2048)
# %%
# Execute Spatial Pooling algorithm over input space.
spatial_pooler = []
for i in encoding:
    sp.compute(encoding[0], True, activeColumns)
    activeColumnIndices = np.nonzero(activeColumns)[0]
    spatial_pooler += [activeColumnIndices]


import pandas as pd
df = pd.DataFrame.from_records(spatial_pooler)

# %%
sp_time = np.zeros([500,1000])
for i in xrange(1000):
    tmp =  spatial_pooler[i][spatial_pooler[i]<500]
    sp_time[tmp,i]=1

import matplotlib.pyplot as plt
plt.imshow(sp_time)
df = pd.DataFrame.from_records(sp_time)

df.plot()
