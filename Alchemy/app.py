from flask import Flask, render_template, jsonify, request
from matplotlib import style
style.use('fivethirtyeight')
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, INTEGER, MetaData, TEXT, FLOAT

app = Flask(__name__)

@app.route('/')
def homePage():
    global engine, measurement, station
    return render_template('home.html')

@app.route('/api/v1.0/precipitation')
def precipitation():
    global engine, measurement, station
    session = Session(engine)
    precipitacionScores = session.query(
        measurement.columns.date,
        measurement.columns.prcp
    )
    data = dict(precipitacionScores)
    session.close()
    data = jsonify(data)
    return data

@app.route('/api/v1.0/stations')
def stations():
    global engine, measurement, station
    session = Session(engine)
    totalStations = session.query(
        station.columns.id,
        station.columns.station
    ).group_by(
        station.columns.station
    )
    data = dict(totalStations)
    session.close()
    data = jsonify(data)
    return data

@app.route('/api/v1.0/tobs')
def tobs():
    global engine, measurement, station
    session = Session(engine)
    tobs = session.query(
        measurement.columns.date,
        measurement.columns.tobs
    )
    data = dict(tobs)
    session.close()
    data = jsonify(data)
    return data

@app.route('/api/v1.0/<start>')
def startTobs(start = '2010-01-01', end = '2017-08-23'):
    global engine, measurement, station
    session = Session(engine)
    tobs = session.query(
        measurement.columns.date,
        measurement.columns.tobs
    ).filter(
        measurement.columns.date >= start,
        measurement.columns.date <= end
    )
    data = dict(tobs)
    session.close()
    data = jsonify(data)
    return data

@app.route('/api/v1.0/<start>/<end>')
def startEndTobs(start = '2010-01-01', end = '2017-08-23'):
    global engine, measurement, station
    session = Session(engine)
    tobs = session.query(
        measurement.columns.date,
        measurement.columns.tobs
    ).filter(
        measurement.columns.date >= start,
        measurement.columns.date <= end
    )
    data = dict(tobs)
    session.close()
    data = jsonify(data)
    return data

engine = create_engine(
        "sqlite:///hawaii.sqlite"
    )
Base = automap_base()
Base.prepare(
        engine,
        reflect=True
    )
measurement = Table('measurement', MetaData(),
                        Column(
                            'id',
                            INTEGER(),
                            primary_key=True,
                            nullable=False
                        ),
                        Column(
                            'station',
                            TEXT()
                        ),
                        Column(
                            'date',
                            TEXT()
                        ),
                        Column(
                            'prcp',
                            FLOAT()
                        ),
                        Column(
                            'tobs',
                            FLOAT()
                        ),
                        schema=None)
station = Table('station', MetaData(),
                    Column(
                        'id',
                        INTEGER(),
                        primary_key=True,
                        nullable=False
                    ),
                    Column(
                        'station',
                        TEXT()),
                    Column(
                        'name',
                        TEXT()
                    ),
                    Column(
                        'latitude',
                        FLOAT()
                    ),
                    Column(
                        'longitude',
                        FLOAT()
                    ),
                    Column(
                        'elevation',
                        FLOAT()
                    ),
                    schema=None
    )
if __name__ == '__main__':
    app.run()