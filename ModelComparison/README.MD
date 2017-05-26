# Model Comparison

Included here are a selection of csv files and the code needed to run them as
well as visualize their results using python 2.7

## CSV Files
- Prfchck_Fndngs_2H.csv
  - Counts the total number of findings per two hour period in the hospital
- Trnstl_103_ST_CORONA.csv
  - Counts the total number of people who have entered the 103rd St Corona Plaza
  subway station every 4 hours


## HTM Model
The hierarchical temporal memory (HTM) model was developed by numenta to analyze
predict and detect anaomalies in time series data.  Information about this model
can be found on their [Github page](https://github.com/numenta/nupic).  To run
their model you will need to install their software

    pip install nupic

You **DO NOT** need to install nupic to visualize the HTM ouput, but you will
need to have pandas and matplotlib installed

To run the HTM model on the data, which needs to be in the same format as the two
privded csv files, you need to call the file as described below.  This will
output a csv file name `FileName_HTM.csv`.  The outputs of the given csv files
are included.

    python HTM_anomaly.py FileName.csv

To visualize the output of the HTM model, call:

    python HTM_Plot.py FileName_HTM.csv

This will produce a python plot which shows the original and predicted values on
the top plot, and the anomaly score and anomaly likelihood in the bottom plot.
For the most part you only need to care about the anomaly likelihood and can
ignore the anomaly score.  The highlighted sections of the graph
represent sections in which the anomaly likelihood was at least 0.999.

![HTM Plot](https://github.com/mseinstein/HTM/blob/master/ModelComparison/HTMplotExample.png)
