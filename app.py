#import libraries
from flask import Flask, jsonify
import pandas as pd
import datetime as dt
from datetime import date
from dateutil.relativedelta import relativedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#create engine and classes
engine = create_engine("sqlite:///RocketLeague.db")
inspector = inspect(engine)
inspector.get_table_names()
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

players = Base.classes.games_by_players_clean
teams = Base.classes.games_by_teams_clean
main = Base.classes.main_clean

session = Session(engine)


#create variables for most recent recording date, date 12 months prior, and station with most recordings
#latest_recording = (session.query(Measurement.date).order_by(Measurement.date.desc()).first()).date
#last_12m_iso = date.fromisoformat(latest_recording)- relativedelta(years=1)
#last_12m = date.isoformat(last_12m_iso)

#top_station = (session.query(func.count(Measurement.date),Measurement.station).\
#    group_by(Measurement.station).\
#    order_by(func.count(Measurement.date).desc()).first()).station



#################################################
# Flask Setup
#################################################
# @TODO: Initialize your Flask app here
# YOUR CODE GOES HERE
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

#Home page with route ids
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return(f"<h1>Project 2 - Rocket League</h1><hr>"
          "<p>by Cheng, Musah, and Dion</p>"
           "<hr><strong>Do not use for data exploration! Due to size of datasets load times are slow 30s + </strong>"
          "<p>/api/v1.0/raw_main</p>"
          "<p>/api/v1.0/raw_players</p>"
          "<p>/api/v1.0/raw_teams</p>") 

# page for last 12 months of percipitation data
@app.route('/api/v1.0/raw_main')
def main_raw_data():
    stmt = session.query(main).statement
    df2 = pd.read_sql_query(stmt, session.bind).dropna()
    
    return jsonify(df2.to_dict())

@app.route('/api/v1.0/raw_players')
def players_raw_data():
    stmt = session.query(players).statement
    df2 = pd.read_sql_query(stmt, session.bind).dropna()
    
    return jsonify(df2.to_dict())

@app.route('/api/v1.0/raw_teams')
def team_raw_data():
    stmt = session.query(teams).statement
    df2 = pd.read_sql_query(stmt, session.bind).dropna()
    
    return jsonify(df2.to_dict())

@app.route('/api/v1.0/test')
def test():
    stmt = session.query(main.game_id).statement
    df2 = pd.read_sql_query(stmt, session.bind).dropna()
    
    return jsonify(df2.to_dict())


if __name__ == "__main__":
    app.run(debug=True)
