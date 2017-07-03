# -*- coding: utf-8 -*-
"""
Created on Mon Jul 03 18:42:04 2017

@author: BJ
"""

import pandas as pd


ED = pd.read_csv('E:\Datasets\ERVisitsWide2010to2017.csv')
ED.TRIAGED = pd.to_datetime(ED.TRIAGED,format="%Y-%m-%d %H:%M:%S",errors ="coerce")
ED = ED[ED.TRIAGED<'2017-07-04']

ED_Fac1 = ED[ED.FACILITYID == 1]
