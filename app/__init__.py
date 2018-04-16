import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from modules import database
from datetime import datetime
import json

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

@app.route('/viz', methods=['GET', 'POST'])
def viz():
	viewType = request.args.get('view', 'location')
	# if request.method == 'POST':
	# 	dateStr = request.form.get('date', None)
	# else:
	dateStr = request.args.get('date', None)

	if dateStr and dateStr != "None":
		date = datetime.strptime(dateStr, '%Y-%m-%d')
	else:
		date = datetime.today()

	if viewType == 'location':
		title = "Patient's Location"
		vizFile = 'locationView.js'
		vizData = database.getAllLocationsAtDate(date)
		print(vizData)
		# vizData = []
		# for location, times in locationData.enumerate():
		# 	for time in times:
		# 		vizData.append({'location': location, 'startTime': time[0], 'endTime': time[1]})
	elif viewType == 'activity':
		title = "Patient's Activities"
		vizFile = 'activityView.js'
		vizData = database.getAllActivities()
	elif viewType == 'sensor':
		title = "Active Sensors and Patient's Location"
		vizFile = 'sensorView.js'
		vizData_sensors = database.getAllDevicesAtDate(date)
		print(vizData_sensors)
		vizData_location = database.getAllLocationsAtDate(date)

		# for sensor, times in sensorData.enumerate():
		# 	for time in times:
		# 		vizData_sensors.append({'location': location, 'startTime': time[0], 'endTime': time[1]})

		# for location, times in locationData.enumerate():
		# 	for time in times:
		# 		vizData_location.append({'location': location, 'startTime': time[0], 'endTime': time[1]})
		
		vizData = [vizData_sensors, vizData_location]
	else:
		return redirect('/viz')

	dates = ['2018-04-15','2018-04-14','2018-04-13']

	return render_template('viz.html', view=viewType, date=dateStr, dateOptions=dates, javascriptFile=vizFile, dataset=json.dumps(vizData), title=title)