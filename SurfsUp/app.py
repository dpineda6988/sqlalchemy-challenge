# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///SurfsUp\Resources\hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
# Initialize Flask app
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Set re-usable variables and functions that can be referenced or called by each individual route
# Define a function that changes the datatype for a date into datetime.date()
def format_date(date):
    return dt.datetime.strptime(date, '%Y-%m-%d').date()

# Determine the dates of the most recent and oldest data point in the dataset and store them in variables 'most_recent_date' and 'oldest_date'
most_recent_date = format_date((session.query(func.max(measurement.date)).all())[0][0])
oldest_date = format_date((session.query(func.min(measurement.date)).all())[0][0])

# Determine the date that is one year prior to the most recent date in the dataset and store it in variable 'recent_one_year_prior_date'
recent_one_year_prior_date = most_recent_date - dt.timedelta(days=365)


# Define the static route for the main homepage that lists the available routes
@app.route("/")
def home():
    return (
        f"<strong>Welcome to the SurfsUp API!</strong><br/><br/>"
        f"<u>Available routes:</u><br/><br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"/api/v1.0/&ltstart&gt &nbsp <strong>or</strong> &nbsp /api/v1.0/&ltstart&gt/&ltend&gt<br/><br/>"
        f"**<strong>Note:</strong> &ltstart&gt and &ltend&gt are dates formatted YYYY-MM-DD**"
    )

# Define static route that queries the last 12 months of preciptation data in the dataset and returns it as a JSON dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Perform a query to retrieve the data and precipitation scores for the last 12 months available in the dataset
    data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= recent_one_year_prior_date).all()

    # Create dictionary 'precip_dict' and fill it by looping through the query 'data' where the dictionary key is 'date' and value is 'prcp'
    precip_dict = {}
    for date, prcp in data:
        precip_dict[date] = prcp

    # Return dictionary 'precip_dict' as a JSON
    return jsonify(precip_dict)

# Create static route that returns a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    # Query a list of the stations from the table 'stations'
    all_stations = session.query(station.station).all()

    # Convert list of tuples into normal list
    all_stations_list = list(np.ravel(all_stations))

    # Return list of stations as a JSON
    return jsonify(all_stations_list)

# Create static route that queries the dates and temperature observations of the most-active station from the last year of available data and return it as a JSON list
@app.route("/api/v1.0/tobs")
def tobs():
    # Query a list of the stations and their counts in descending order.
    station_counts = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    # The first station listed is the most active station so save the station id in variable 'most_active_station_id'
    most_active_station_id = station_counts[0][0]
    # Query the dates and temperature observations for the most active station recorded over the last 12 months in the dataset
    observation_query = session.query(measurement.date, measurement.tobs).filter(measurement.station == most_active_station_id).filter(measurement.date >= recent_one_year_prior_date).all()

    # Create a list to hold the temperature observations
    temp_observations_list = []
    # Loop through the query of dates and temperature observations and store them as individual dictionaries that are then appended to the temp_observations_list 
    for date , tobs in observation_query:
        temp_observation = {}
        temp_observation["date"] = date
        temp_observation["tobs"] = tobs
        temp_observations_list.append(temp_observation)

    # Return the list of temp observations as a JSON
    return jsonify(temp_observations_list)

# Create a dynamic route that will return a JSON list of the minimum temperature, average temperature, and maximum temperature for a specified start or start-end date range
# Set route URLs for start date only and start date with end date
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
# Define a function where the default value for variable 'end' is None (meaning it would apply to the URL with start date only)
def date_range_stats(start, end=None):
    # Convert 'start' into datetime datatype or return an error if a properly formatted date is not provided
    try:
        start_date = format_date(start)
    except ValueError:
        return jsonify([{'error': 'Invalid date format for start date'}])
    
    # If a value for 'end' was provided, convert into datetime datetime datatype or return an error if a properly formatted date is not provided
    if end:
        try:
            end_date = format_date(end)
        except ValueError:
            return jsonify([{'error': 'Invalid date format for end date'}])   
    # If a value for end is not provided and defaulted to None, re-assign it as the most recent date in the dataset (most_recent_date)
    else:
        end_date = most_recent_date    
    
    # Check if the provided date falls within the date range of the data set else return an error
    if start_date > most_recent_date or start_date < oldest_date:
        return jsonify([{'Error': 'Start date outside of dataset range'}])
    if end_date > most_recent_date or end_date < oldest_date:
        return jsonify([{'Error': 'End date outside of dataset range'}])
    
    # Check that the end date does not come before the start date or return an error
    if start_date > end_date:
        return jsonify([{'Error': 'End date must occur after the start date'}])

    # Query the mininmum temperature, max temperature, and average temperature by date for the date range that falls between defined date ranges as per variables 'start_date' and 'end_date'
    temp_stats_query = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).group_by(measurement.date).filter(measurement.date >= start_date, measurement.date <=end_date).all()
    
    # Create a list to hold the temperature stats
    temp_stats_list = []
    # Loop through the query of dates and temperature stats and store them as individual dictionaries that are then appended to the temp_observations_list 
    for date, min, max, avg in temp_stats_query:
        temp_stats_dict = {}
        temp_stats_dict["date"] = date
        temp_stats_dict["TMIN"] = min
        temp_stats_dict["TMAX"] = max
        temp_stats_dict["TAVG"] = avg
        temp_stats_list.append(temp_stats_dict)

    # Return the populated list as a JSON
    return jsonify(temp_stats_list)

# Create statement to run the app
if __name__ == "__main__":
    app.run(debug=True)