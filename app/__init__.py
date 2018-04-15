import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from modules import database
import datetime

app = Flask(__name__) # create the application instance
app.config.from_object('config.Config') # load config

@app.route('/')
def activity():

	# # Sample SQL Server Query
	# cursor = database.getCursor()
	# rooms = cursor.execute("SELECT * FROM Rooms").fetchall();
	# print(rooms)
	# database.closeConnection()
	#database.getAllDevicesAtDate(datetime.today())
    sensorDict = database.getAllDevicesAtDate(datetime.datetime(2018,4,14,hour=16,minute=30,second=0,microsecond=0))
    locDict = database.getAllLocationsAtDate(datetime.datetime(2018,4,14,hour=16,minute=30,second=0,microsecond=0))
    print(sensorDict['TV'])
    print(sensorDict['TV'][0])
    print(locDict['The Kitchen'])
    print(locDict['The Kitchen'][0])
    
    return render_template('home.html')

@app.route('/viz')
def viz():


	return render_template('index.html')