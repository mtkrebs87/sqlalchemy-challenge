# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"/api/v1.0/startdate2010-01-01<br/>"
        f"/api/v1.0/start/end2017-08-23<br/>"       
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
        
        # Create our session (link) from Python to the DB
        session = Session(engine)

        """Return list for precipitation results for last 12 months"""
        #Convert query results
        results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").\
        filter(measurement.date <= "2017-08-23").all()

        #Close the session
        session.close()

        #Convert list to JSON representation
        precipitation_results = []
        for date, prcp in results:
              precipitation_dict = {}
              precipitation_dict[date] = date
              precipitation_dict[prcp] = prcp
              precipitation_results.append(precipitation_dict)

        return jsonify(precipitation_results)


@app.route("/api/v1.0/stations")
def stations():
      
        #Create session (link) from Python to the DB
        session = Session(engine)

        """Return List of Stations"""
        #Query list of stations
        results_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

        #Close Session
        session.close()

        #Convert to normal list
        station_results = list(np.ravel(results_station))

        return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tobs():
      
        #Creat Session
        session = Session(engine)

        """Return List of date and temps from most active station"""
        #Query dates and temps
        temperature_data = session.query(measurement.date, measurement.tobs).\
                                filter(measurement.date >= "2016-08-23").\
                                filter(measurement.date <= "2017-08-23").\
                                filter(measurement.station == "USC00519281")
        
        #Close Session
        session.close()

        temperature_date = []
        for date, tobs in temperature_data:
              temp_dict = {}
              temp_dict[date] = date
              temp_dict[tobs] = tobs
              temperature_date.append(temp_dict)

        return jsonify(temperature_date)

@app.route("/api/v1.0/start")
def start():
      
        #Create Session
        session = Session(engine)

        """Calculate Tmin, Tavg, Tmax for all dates"""
        start_date = session.query(measurement.date >= "2010-01-01")
        end_date = session.query(measurement.date <= "2017-08-23")

        #Query for t-test results
        results = session.query(func.min(measurement.tobs), func.max(measurement.tobs).\
                                func.avg(measurement.tobs)).filter(measurement.date >= start_date).all()
        
        start_all = []
        for min, max, avg in results:
               start_dict = {}
               start_dict["min"] = min
               start_dict["max"] = max
               start_dict["avg"] = avg
               start_all.append(start_dict)

        return jsonify(start_all)

@app.route("api/v1.0/start/end")
def start_end():
       
    #Create Session
        session = Session(engine)

        """Calculate Tmin, Tavg, Tmax for all dates"""
        start_date = session.query(measurement.date >= "2010-01-01")
        end_date = session.query(measurement.date <= "2017-08-23")

        #Query for t-test results
        results = session.query(func.min(measurement.tobs), func.max(measurement.tobs).\
                                func.avg(measurement.tobs)).filter(measurement.date <= end_date).all()
        
        start_end_all = []
        for min, max, avg in results:
               start_end_dict = {}
               start_end_dict["min"] = min
               start_end_dict["max"] = max
               start_end_dict["avg"] = avg
               start_end_all.append(start_end_dict)

        return jsonify(start_end_all)




#Stop Flask
if __name__ == '__main__':
    app.run(debug=True)
