# 1. import 
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
#calc temp funtion
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# 3. Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")
def precipitation():
    analysis = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.date <= "2017-08-23").all()
    analysis_dict = dict(analysis)
    return jsonify(analysis_dict) 
# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/stations")
def stations():
    station_list  = session.query(Measurement.station).group_by(Measurement.station).all()    
    return jsonify(station_list)
# tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").all()
    return jsonify(tobs)
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def range_temp(start, end=""):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        range_temp = session.query(*sel).filter(Measurement.date >= start).all()
        return jsonify(range_temp)   
        
    range_temp = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify(range_temp)

if __name__ == "__main__":
    app.run(debug=True)
