import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from modules import database
from datetime import datetime

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
	

	return render_template('home.html')

@app.route('/viz')
def viz():
	

	return render_template('index.html')