import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite") 

Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement= Base.classes.measurement

app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()
    
    all_dates = []
    for date, prcp in results:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["percipitation"] = prcp
        all_dates.append(rain_dict)

    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)

    results=session.query(Measurement.tobs).\
    filter(Measurement.station=='USC00519281').\
    filter(Measurement.date >= dt.date(2016,8,23)).all()

    session.close()

    all_temps = list(np.ravel(results))

    return jsonify(all_temps)


@app.route("/api/v1.0/<start>")
def start_end_temps(start):
    session = Session(engine)
    
    start= dt.datetime.strptime(start, '%Y-%m-%d')

    temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    temps = list(np.ravel(temp))
    return jsonify(temps)



@app.route("/api/v1.0/<start>/<end>")
def start_temps(start,end):
    session = Session(engine)
    
    start= dt.datetime.strptime(start, '%Y-%m-%d')
    end = dt.datetime.strptime(end, '%Y-%m-%d')
    temp = session.query(func.min(Measurement.tobs), 
                         func.avg(Measurement.tobs), 
                         func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(temp))
    return jsonify(temps)



if __name__ == '__main__':
    app.run(debug=True)