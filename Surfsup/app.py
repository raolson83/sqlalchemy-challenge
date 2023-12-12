# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value"""
    # Query 
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    past_year = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        past_year.append(precip_dict)

    return jsonify(past_year)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    # Query 
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_set = list(np.ravel(results))

    return jsonify(station_set)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most-active station for the previous year of data"""
    # Query 
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago).filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    # Create a dictionary from the row data and append to a list
    most_active = []
    for station, date, tobs in results:
        temp_dict = {}
        temp_dict['station'] = station
        temp_dict['date'] = date
        temp_dict['tobs'] = tobs
        most_active.append(temp_dict)

    # temps = list(np.ravel(results))

    return jsonify(most_active)


@app.route('/api/v1.0/<start>')
def start(start):
    start = datetime.strptime(start, "%m-%d-%Y").date()

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    # Query 
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    starts = list(np.ravel(results))

    return jsonify(starts)


@app.route("/api/v1.0/<start>/<end>")
def startsends(start, end):
    start = datetime.strptime(start, "%m-%d-%Y").date()
    end = datetime.strptime(end, "%m-%d-%Y").date()

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    # Query 
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    startsends = list(np.ravel(results))

    return jsonify(startsends)

if __name__ == '__main__':
    app.run(debug=True)