# Data Sets

Here are a compilation of online data sets which have patterns similar to what
we are interested in modeling.

## [Archived NYC Real Time Traffic Speed Data Feed](http://data.beta.nyc/dataset/nyc-real-time-traffic-speed-data-feed-archived)
 - Data feed contains 'real-time' traffic information from locations where DOT picks up sensor feeds within the five boroughs, mostly on major arterials and highways, using 5 minute snapshots.
 - Archived version of the streaming info from [here](https://data.cityofnewyork.us/Transportation/Real-Time-Traffic-Speed-Data/xsat-x5sa)
 - Included here, as Traffic2016_Narrow.7z, is the data from 2016 but just the Id,
 Speed, Travel time and DataAsOf fields


   | Field | Definition| Format |
   |-------|-----------|-----|
   | Id | TRANSCOM Link ID|Int|
   | Speed | Average speed a vehicle traveled between end points on the link in the most recent interval| Float|
   | TravelTime | Time the average vehicle took to traverse the link| Int|
   |Status | Artifact – not useful| Int|
   | DataAsOf | Last time data was received from link| String format %m/%d/Y %H:%M:%S| 
   | linkId| TRANSCOM Link ID (same as ID field)| Int|


## [MTA turnstile Data](http://web.mta.info/developers/turnstile.html)
