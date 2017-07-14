# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:45:21 2017

@author: msnow1
"""


from HTMPkg.sdr_encoder import sdr_encoder
from HTMPkg.sp import spatial_pooler
from HTMPkg.tm import temporal_memory

file_name = "E:\\MyDocuments\\GitHub\\HTM\\AlgorithmComponents\\Data\\appt_htm_0steps.csv"
encoding = sdr_encoder(file_name).create_encoding()
sp = spatial_pooler(encoding).output_sp()
tm = temporal_memory(sp).output_tm()



import numpy as np
sp_time = np.zeros([400,1000])
for i in xrange(1000):
    tmp =  sp[i][sp[i]<400]
    sp_time[tmp,i]=1

import matplotlib.pyplot as plt
plt.imshow(sp_time)