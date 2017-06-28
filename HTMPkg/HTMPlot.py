import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.dates import date2num, DateFormatter
import numpy as np


DATA_DIR = "."
ANOMALY_THRESHOLD = 0.999
HIGHLIGHT_ALPHA = 0.3
ANOMALY_HIGHLIGHT_COLOR = 'red'


def lookup(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date:pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)


def ImportData(inputData):
    """
    Imports the csv file, converts the timestamp column to dateformat
    and creates a column which converts the dates into numeric values
    for plotting purposes
    """
    DataFl = pd.read_csv(inputData, na_values="")
    DataFl['timestamp'] = lookup(DataFl['timestamp'])
    DataFl['dates'] = [date2num(date) for date in DataFl['timestamp']]
    return DataFl

def extractAnomalyIndices(anomalyLikelihood):
  anomaliesOut = []
  anomalyStart = None
  for i, likelihood in enumerate(anomalyLikelihood):
    if likelihood >= ANOMALY_THRESHOLD:
      if anomalyStart is None:
        # Mark start of anomaly
        anomalyStart = i
    else:
      if anomalyStart is not None:
        # Mark end of anomaly
        anomaliesOut.append((
          anomalyStart, i, ANOMALY_HIGHLIGHT_COLOR, HIGHLIGHT_ALPHA
        ))
        anomalyStart = None

  # Cap it off if we're still in the middle of an anomaly
  if anomalyStart is not None:
    anomaliesOut.append((
      anomalyStart, len(anomalyLikelihood)-1,
      ANOMALY_HIGHLIGHT_COLOR, HIGHLIGHT_ALPHA
    ))

  return anomaliesOut
    
def highlightChart(highlights, dates, chart):
    #chartHighlights = []
    for highlight in highlights:
      # Each highlight contains [start-index, stop-index, color, alpha]
      chart.axvspan(dates[highlight[0]], dates[highlight[1]],
        color=highlight[2], alpha=highlight[3])
      

def PlotData(InputName):
    """
    Assumes the InputName corresponds a like-named CSV file in 
    the current directory.
  
    :param InputName: Important for finding model params and input CSV file
    """
    inputData = "%s/%s" % (DATA_DIR, InputName.replace(" ", "_"))
    DataFl = ImportData(inputData) 
    anomalies = extractAnomalyIndices(DataFl['anomaly_likelihood'].tolist())
    Resid = DataFl.prediction-DataFl[DataFl.columns[1]]
    AbsPrcntEr = abs(Resid)/DataFl[DataFl.columns[1]]
    AbsPrcntEr[np.isinf(AbsPrcntEr)] = float('NaN')
    SqEr = Resid**2
#    CumAvg = [0]
#    ValCt = 0
#    for i in AnomScr:
#        ValCt += 1
#        CumAvg += [CumAvg[-1] + (i - CumAvg[-1])/ValCt]
#        if np.isnan(CumAvg[-1]):
#            CumAvg[-1] =0 
#    CumAvg = CumAvg[1:]
#    
    MAPE = [0]
    MovWin = 240
    MSE = [0]
    StrtCt = -1
    for i in range(len(AbsPrcntEr)):
        if np.isnan(AbsPrcntEr[i]) and i < MovWin:
            StrtCt += 1
            MAPE += [0]
            MSE += [0]
        elif np.isnan(AbsPrcntEr[i]):
            AbsPrcntEr[i] = AbsPrcntEr[i-1]
            MAPE += [MAPE[-1]]
            MSE += [MSE[-1]]
        elif i-StrtCt <= MovWin:
            MAPE += [MAPE[-1] + (AbsPrcntEr[i] - MAPE[-1])/(i-StrtCt)]
            MSE += [MSE[-1] + (SqEr[i] - MSE[-1])/(i-StrtCt)]
        else:
            if np.isnan(AbsPrcntEr[i-MovWin]):
                MAPE += [MAPE[-1] + (AbsPrcntEr[i])/MovWin]
            else:
                MAPE += [MAPE[-1] + (AbsPrcntEr[i] - AbsPrcntEr[i-MovWin])/MovWin]
            MSE += [MSE[-1] + (SqEr[i] - MSE[i-MovWin])/MovWin]
    MAPE = MAPE[1:]
    MSE = MSE[1:]
#            MovAvg2 += [np.nanmean(AnomScr[:i+1])]
#        if np.isnan(MovAvg[-1]):
#            MovAvg[-1] =0 
    #plt.ion()
    #fig = plt.figure(figsize=(8, 6))
#    DataFl['CumAvg'] = CumAvg
    DataFl['MAPE'] = MAPE
    DataFl['MSE'] = MSE
    
    gs = gridspec.GridSpec(2,1, height_ratios=[3, 1]) 
    ax0 = plt.subplot(gs[0])
    ax01 = ax0.twinx()
    ax1 = plt.subplot(gs[1], sharex=ax0)
    #ax1.set_color_cycle(['m', 'r'])
    ax1.set_prop_cycle('color',['m', 'r','g'])
    ax01.set_prop_cycle('color',['g'])
    
#    MainGraph = DataFl.plot(x = 'dates', y=[DataFl.columns[1],'prediction','MSE'], ax = ax0)
    MainGraph = DataFl.plot(x = 'dates', y=[DataFl.columns[1],'prediction'], ax = ax0)
    MainGraphR = DataFl.plot(x = 'dates', y='MSE', ax = ax01)
    AnomalyGraph = DataFl.plot(x = 'dates', y=['anomalyScore','anomaly_likelihood','MAPE'], ax=ax1)
    
    dateFormatter = DateFormatter('%m/%d/%y')
    MainGraph.xaxis.set_major_formatter(dateFormatter)
    MainGraphR.xaxis.set_major_formatter(dateFormatter)
    AnomalyGraph.xaxis.set_major_formatter(dateFormatter)
    
    ax0.set_ylabel(DataFl.columns[1])
    ax01.set_ylabel('MSE 30 days', color = 'g')
    ax1.set_ylabel('Percent')
    ax1.set_xlabel('Dates')
    
    # Highlight anomalies in anomaly chart
    highlightChart(anomalies, DataFl['dates'], MainGraph)
    highlightChart(anomalies, DataFl['dates'], AnomalyGraph)
    
#    MainGraph.legend(tuple(['actual', 'predicted','MSE 30 days']), loc=4)
    MainGraph.legend(tuple(['actual', 'predicted']), loc=4)
    AnomalyGraph.legend(tuple(['anomaly score','anomaly likelihood','MAPE 30 days']), loc=4)
    MainGraphR.legend_.remove()    
    #plt.draw()
    #plt.ioff()
    ax0.set_title(InputName)
    plt.draw()
    plt.show()

# %%

if __name__ == "__main__":
    args = sys.argv[1:]
    INPUT_FILE = args[0]    
    try: 
        INPUT_FILE
    except NameError:
        raise ValueError('Need to enter the name of a csv file as an argument')
    PlotData(INPUT_FILE)