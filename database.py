import pyodbc
from config import Config

_conn = None


def getConnection():
	global _conn
	if _conn is None:
		connectionString = 'DSN={};DATABASE={};UID={};PWD={}'.format(Config.DATABASE_HOST,Config.DATABASE_DB,Config.DATABASE_USER,Config.DATABASE_PASSWORD)
		_conn = pyodbc.connect(connectionString)

	return _conn

def getCursor():
	global _conn
	try:
		cursor = _conn.cursor()
	except:
		getConnection()
		cursor = _conn.cursor()

	return cursor

def closeConnection():
	global _conn
	if _conn is not None:
		try:
			_conn.cursor.close()
			_conn.close()
			_conn = None
		except:
			_conn = None