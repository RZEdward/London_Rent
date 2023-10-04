Welcome to my second (published) project! This was built to deliver insights on the spareroom.com monthly rental prices in each borough, and also presents some key lifestyle metrics designed to guide someone moving to London for the first time.

General Steps:

- Develop a Python script (scraper.py) that pulls all of the listing prices from each borough on spareroom.com
- Store the statistical data (mean, max, min, median, stdev, count etc) in borough_stats.csv
- Store all of the listings in prices.csv - this is key - need to reduce dimensionality + allow for a join to other csv's so I can make use of Tableau's boxplot chart feature later
- Create an Excel workbook
- Import borough_stats.csv to Excel
- While in Excel, add in more columns for population, area, green area, pubs, pub density etc etc drawn from many different sources - most of this data was manually typed in (just made sense in this instance)
- Save this Excel sheet as stats.csv
- Download spatial/map data for London and its boroughs (.shp file and associated)
- Open Tableau
- Import stats.csv, prices.csv, & map data as data sources
- Join data sources on the borough names
- Create sheets covering rental prices, knife crime, green coverage, median age, commuter satisfaction, pub area density + rankings table
- Note that defining commute time from a region as wide as a whole borough is not as simple as it seems - even if you make the very general assumption that everyone commutes to central london, the specific tube station(s) selected as references, as well as varying walk times to the home boroughs station can vary data dramatically
- I think it is more logical to assess lifestyle in each borough and commute experience, and then allow any dashboard viewer to eliminate boroughs based on their personal commute requirements
- Then make our dashboard and publish it to Tableau Public + my personal website
