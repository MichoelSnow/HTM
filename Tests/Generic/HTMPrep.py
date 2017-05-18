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


ParamStrRpl = ['VariableNm','VariableMinVal','VariableMaxVal']

def EditFiles(INPUT_FILE):
    # Get the new parameters from the csv file
    NewStr = getNewParams(INPUT_FILE)
    # Read in the file
    ParamsFile = '.\model_params\model_params.py'
    with open(ParamsFile, 'r') as file:
      Paramdata = file.read()
    # Replace the target string
    for pos,OldStr in enumerate(ParamStrRpl):
        Paramdata = Paramdata.replace(OldStr, NewStr[pos])
    
    
    ParamOutput = ".\model_params\%s_model_params.py" % INPUT_FILE[:-4]
    # Write the file out again
    with open(ParamOutput, 'w') as file:
        file.write(Paramdata)
        
    RunFile = 'run_anomaly.py'
    with open(RunFile, 'r') as file:
      Rundata = file.read()
    
    # Replace the target string
    Rundata = Rundata.replace('PredFldNm', NewStr[0])
    
    
    RunOutput = "run_anomaly_%s.py" % INPUT_FILE[:-4]
    # Write the file out again
    with open(RunOutput, 'w') as file:
        file.write(Rundata)  
    

        
        

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
    return [CsvCol[1],csvMin,csvMax]
  
  
if __name__ == "__main__":
    args = sys.argv[1:]
    INPUT_FILE = args[0]    
    try: 
        INPUT_FILE
    except NameError:
        raise ValueError('Need to enter the name of a csv file as an argument')
    EditFiles(INPUT_FILE)