# sqlalchemy-challenge
# SurfsUp

An analysis of data stored in a SQLite database conducted via a jupyter notebook leveraging the SQLAlchemy Python library and a Flask API created using the queries derived from the analysis.

## Description

To help plan for a hypothetical trip to Honolulu, Hawaii, an exploratory analysis was conducted using a SQLite database containing data gathered from several weather stations in the area.  Using a jupyter notebook, the following variables and topics were analyzed and explored:

#### Precipitation Analysis
The latest 12 months of measured precipitation data (in inches) in the datset was queried and analyzed via a bar plot and general summary statistics

#### Weather Station Analysis
The total number of distinct weather stations in the dataset was quieried and then ordered based upon the the number of observations per station.  Based on this ranking, the most active weather station was identified.  Focusing on specifically on data from the most active station, the lowest, highest, and average temperatures were calculated.  The latest 12 months of temperature observations (TOBS) for this station was then queried and then plotted as a histogram.

#### API
A Flask API was then created based on the queries dervied from the above analysis.  Using Python, the API was coded to have the following routes:
1. A static route to the homepage listing all the available routes
2. A static route that displays the latest 12 months of precipitation data, displayed as a JSON dictionary where date is the key and the measured precipation is the value
3. A static route that displays a JSON list of all weather stations from the dataset
4. A static route that displays a JSON list of temperature observations for the latest 12 months
5. A dynamic route that displays a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.


### Dependencies
* Python with the following libraries: SQLAlchemy, pandas, numpy, datetime - file name 'app.py'
* jupyter notebook - file name 'climate_starter.ipynb'
* Flask
* The following SQLite database file is required to connect to:
    * hawaii.sqlite
* Any web browser program to view the URL routes from 'app.py'

### Installing & Execution
Once the necessary programs and libraries are installed, the SurfsUp directory can be downloaded to execute the main files ('climate_starter.ipynb' and 'app.py').  Note that since the main files contain relative file paths, it is important that the file locations within the SurfsUp directory are not changed in order for the main files to execute properly.

## Authors

Daniel Pineda

## Acknowledgments
SurfsUp was created as an assignment for the University of California, Irvine Data Analytics Bootcamp - June 2024 Cohort under the instruction and guidance of Melissa Engle (Instructor) and Mitchell Stone (TA).
The practical exercises and coding examples demonstrated through the bootcamp helped inform and inspire the code for this project.

Additionally, the following resources were used for further reference:

Xpert Learning Assistant - UCI's AI-powered learning assistant - referenced for how to reset the number of tick labels along an axis in a pyplot ('climate_starter.ipynb - code cell 10)
