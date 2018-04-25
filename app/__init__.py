import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from modules import database
from datetime import datetime
import json

app = Flask(__name__) # create the application instance
app.config.from_object('config.Config') # load config


activities = ["Sleeping", "Cooking", "Entertainment"]
sensors = [[],["Stove","Refrigerator"],["TV","X Box 360"]]
locations = ["Bedroom Two","The Kitchen","The Livingroom"]


@app.route('/')
def activity():
	allActivities = list(database.getAllActivityLocations().keys())
	allSensors = list(database.getLocationsOfDevices().keys())
	allLocations = list(database.getDevicesAtAllLocations().keys())
	print(allActivities)
	print(allSensors)
	print(allLocations)
	print(activities)
	print(sensors)
    
	return render_template('activities.html', allActivities=allActivities, allSensors=allSensors, activities=activities, sensors=sensors)

@app.route('/addActivities', methods=['POST'])
def addActivities():
	global activities
	global sensors
	global locations
	activities = []
	sensors = []
	locations = []
	activityLocations = database.getAllActivityLocations()

	for i in range(3):
		index = i+1
		activity = request.form.get('activity'+str(index), None)
		if activity:
			activities.append(activity)
			locations.append(activityLocations[activity])
			sensorSet = request.form.getlist('sensor-activity'+str(index)+'[]')
			sensors.append(sensorSet)

	print(activities)
	print(sensors)
	print(locations)

	return json.dumps({})


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
		vizData_sensors = database.getAllDevicesAtDate(date)
		vizData_location = database.getAllLocationsAtDate(date)
		sensorList = []
		for sensorSet in sensors:
			for sensor in sensorSet:
				sensorList.append(sensor.replace(' ','_'))

		vizData = database.getAllActivities(sensorList, locations, activities, vizData_sensors, vizData_location)
	elif viewType == 'sensor':
		title = "Active Sensors and Patient's Location"
		vizFile = 'sensorView.js'
		vizData_sensors = database.getAllDevicesAtDate(date)
		vizData_location = database.getAllLocationsAtDate(date)
		vizData_sensors_locations = database.getDevicesAtAllLocations()


		#vizData = database.getAllActivities(['stove'],['kitchen'],['cooking'],vizData_sensors,vizData_location)
		vizData = [vizData_location, vizData_sensors, vizData_sensors_locations]
	else:
		return redirect('/viz')

	dates = ['2018-04-15','2018-04-14','2018-04-13']

	return render_template('viz.html', view=viewType, date=dateStr, dateOptions=dates, javascriptFile=vizFile, dataset=json.dumps(vizData), title=title)