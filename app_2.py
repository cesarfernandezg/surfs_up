# 9.5.1 Set Up the Database and Flask
# SET UP FLASK WEATHER APP
# import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# add SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# add Flask dependencies
from flask import Flask, json, jsonify

# SET UP THE DATABASE
# access SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect tables
Base = automap_base()
# reflect the database
Base.prepare(engine, reflect = True)

# save references to each table and assign them to variables
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# SET UP FLASK
# define the Flask app
app = Flask(__name__)

# 9.5.2 Create the Welcome Route
# define the welcome route
@app.route("/")

# next step is to add the routing information for each of the other routes

# create a function welcome() with a return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# 9.5.3 Precipitation Route
# build the route for precipitation analysis
@app.route("/api/v1.0/precipitation")
# create the precipitation function
def precipitation():
    #add the line of code that calculates the date one year ago from the most
    # recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # add a query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    # create a dictionary with the date as the key and the precipiation
    # as the value. Use jsonify() function.
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# 9.5.4 Stations Route
# define the route and the route name
@app.route("/api/v1.0/stations")
# create function stations()
def stations():
  # create query that allow get all of the stations in the database
  results = session.query(Station.station).all()
  # unravel the results into a one-dimensional array. Using function np.ravel()
  stations = list(np.ravel(results)) # convert it into a list
  return jsonify(stations=stations) # jsonify the list and return it as JSON

# 9.5.5 Monthly Temperature Route
# define the route
@app.route("/api/v1.0/tobs")
# create function temp_monthly()
def temp_monthly():
  # calculate the date one year ago from the last date in the database
  prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
  # query the primary station for all the temperature observations from the previous year
  results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
  # unravel the results into a one-dimensional array and convert
  # that array into a list
  temps = list(np.ravel(results))
  return jsonify(temps=temps)

# 9.5.6 Statistics Route
# create route for starting date and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# create function stats()
def stats(start=None, end=None): # add parameters start & end
  # create a query to select the minimum, average, and maximum temperatures
  sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
  # add an if-not statement
  if not end:
    results = session.query(*sel).\
            filter(Measurement.date >= start).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
  # calculate the temperature minimum, average, and maximum
  results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
  temps = list(np.ravel(results))
  return jsonify(temps)
  




