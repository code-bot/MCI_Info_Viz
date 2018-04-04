import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import database

app = Flask(__name__) # create the application instance
app.config.from_object('config.Config') # load config

@app.route('/')
def home():

	# Sample SQL Server Query
	cursor = database.getCursor()
	rooms = cursor.execute("SELECT * FROM Rooms").fetchall();
	print(rooms)
	database.closeConnection()

	return "Home"
