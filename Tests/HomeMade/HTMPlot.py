import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.dates import date2num, DateFormatter


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
    #plt.ion()
    #fig = plt.figure(figsize=(8, 6))
    
    gs = gridspec.GridSpec(2,1, height_ratios=[3, 1]) 
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)
    #ax1.set_color_cycle(['m', 'r'])
    ax1.set_prop_cycle('color',['m', 'r'])
    
    MainGraph = DataFl.plot(x = 'dates', y=[DataFl.columns[1],'prediction'], ax = ax0)
    AnomalyGraph = DataFl.plot(x = 'dates', y=['anomalyScore','anomaly_likelihood'], ax=ax1)
    
    dateFormatter = DateFormatter('%m/%d')
    MainGraph.xaxis.set_major_formatter(dateFormatter)
    AnomalyGraph.xaxis.set_major_formatter(dateFormatter)
    
    ax0.set_ylabel(DataFl.columns[1])
    ax1.set_ylabel('Percent')
    ax1.set_xlabel('Dates')
    
    # Highlight anomalies in anomaly chart
    highlightChart(anomalies, DataFl['dates'], MainGraph)
    highlightChart(anomalies, DataFl['dates'], AnomalyGraph)
    
    MainGraph.legend(tuple(['actual', 'predicted']), loc=3)
    AnomalyGraph.legend(tuple(['anomaly score','anomaly likelihood']), loc=3)    
    #plt.draw()
    #plt.ioff()
    ax0.set_title(InputName)
    plt.draw()
    plt.show()



if __name__ == "__main__":
    args = sys.argv[1:]
    INPUT_FILE = args[0]    
    try: 
        INPUT_FILE
    except NameError:
        raise ValueError('Need to enter the name of a csv file as an argument')
    PlotData(INPUT_FILE)