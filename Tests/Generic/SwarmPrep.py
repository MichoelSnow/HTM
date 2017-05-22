"""
Modifies the generic model_params file to match the settings
of the given csv file 
"""

#import importlib
import sys
#import csv
#import datetime
#import os
#import getpass
#os.environ["USER"] = getpass.getuser()

import pandas as pd
import re


ParamStrRpl = ['VariableNm','VariableMinVal','VariableMaxVal','FlNm']

def EditFiles(INPUT_FILE):
    # Get the new parameters from the csv file
    NewStr = getNewParams(INPUT_FILE)
    # Read in the file
    ParamsFile = '.\swarm_description.py'
    with open(ParamsFile, 'r') as file:
      Paramdata = file.read()
    # Replace the target string
    for pos,OldStr in enumerate(ParamStrRpl):
        Paramdata = Paramdata.replace(OldStr, NewStr[pos])
    
    
    ParamOutput = ".\%s_swarm_description.py" % INPUT_FILE[:-4]
    # Write the file out again
    with open(ParamOutput, 'w') as file:
        file.write(Paramdata)
        
    

        
        

def getNewParams(INPUT_FILE):
    """
    
    """
    CsvData = pd.read_csv(INPUT_FILE)
    CsvData = pd.read_csv(INPUT_FILE)
    CsvCol = CsvData.columns
    CsvData = CsvData[:][2:]
    CsvData[CsvCol[1]] = pd.to_numeric(CsvData[CsvCol[1]])
    csvMax = str(CsvData[CsvCol[1]].max())
    csvMin = str(CsvData[CsvCol[1]].min())
    return [CsvCol[1],csvMin,csvMax,INPUT_FILE]
  
  
if __name__ == "__main__":
    args = sys.argv[1:]
    INPUT_FILE = args[0]    
    try: 
        INPUT_FILE
    except NameError:
        raise ValueError('Need to enter the name of a csv file as an argument')
    EditFiles(INPUT_FILE)