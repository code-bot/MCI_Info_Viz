# MCI_Info_Viz

## Setup
Clone the repo
Open terminal and `cd` into the main repo
To get all the needed libraries, run `pip install -r requirements.txt`

## Running
Make sure you're in the main project directory
In terminal, run `export FLASK_APP=main.py` (mac) or `set FLASK_APP=main.py` (windows)
Then, run `flask run`
You should see:
`* Serving Flask app "main"`
`* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

Open localhost:5000 (http://127.0.0.1:5000/) in browser to see the app

## Flask Tutorial
Checkout this link: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

In a nutshell:
- Python functions with `@app.route(ROUTE)` signature will be run when going to http://127.0.0.1:5000/ROUTE
- Use the `render_template(TEMPLATE_NAME.html)` function to load 'TEMPLATE_NAME.html' from the 'templates' folder
- Use the static folder to hold any static data such as images, css files, or javascript files
- Learn how to use templating: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

## Connecting to Database
pyodbc tutorial for running queries: https://github.com/mkleehammer/pyodbc/wiki/Getting-started

If you have Mac OSX follow these steps to connect to a SQL Server: https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Mac-OSX
- Make sure the server name when using the above steps (the part they label 'MYMSSQL') is 'AwareHomeServer' as specified in 'config.py'

To visualize the database outside of code:
https://docs.microsoft.com/en-us/sql/sql-operations-studio/download
OR
https://www.valentina-db.com/en/studio/download/current

To connect to the database in code, use the 'database.py' file provided.
- Use `getConnection()` function to set up the connection if needed and return the connection
- Use `getCursor()` function to set up the connection if needed and get the cursor to run queries on
- After everything, use `closeConnection()` to close the cursor and connection
An example is provided in 'app/__init__.py' under the 'home' route

