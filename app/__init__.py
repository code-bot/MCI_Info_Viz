import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from modules import database
from datetime import datetime
import json

app = Flask(__name__) # create the application instance
app.config.from_object('config.Config') # load config

@app.route('/')
def activity():
    
    return render_template('home.html')

@app.route('/viz', methods=['GET', 'POST'])
def viz():
	viewType = request.args.get('view', 'location')
	# if request.method == 'POST':
	# 	dateStr = request.form.get('date', None)
	# else:
	dateStr = request.args.get('date', None)

	if dateStr and dateStr != "None":
		date = datetime.strptime(dateStr, '%a, %B %d %Y')
	else:
		date = datetime.today()
		dateStr = date.strftime('%a, %B %d %Y')

	if viewType == 'location':
		title = "Patient's Location"
		vizFile = 'locationView.js'
		vizData = database.getAllLocationsAtDate(date)
	elif viewType == 'activity':
		title = "Patient's Activities"
		vizFile = 'activityView.js'
		vizData = database.getAllActivities()
	elif viewType == 'sensor':
		title = "Active Sensors and Patient's Location"
		vizFile = 'sensorView.js'
		vizData_sensors = database.getAllDevicesAtDate(date)
		vizData_location = database.getAllLocationsAtDate(date)
		vizData_sensors_locations = database.getDevicesAtAllLocations()

		
		vizData = [vizData_location, vizData_sensors, vizData_sensors_locations]
	else:
		return redirect('/viz')

	dates = ['2018-04-15','2018-04-14','2018-04-13']

	return render_template('viz.html', view=viewType, date=dateStr, dateOptions=dates, javascriptFile=vizFile, dataset=json.dumps(vizData), title=title)