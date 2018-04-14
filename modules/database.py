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

def getActivityTimes(sensor, location, sensorDict, locationDict):
	pass

def getAllLocationsAtDate(date):
	pass

def getAllDevicesAtDate(date):
	command = """SELECT DeviceID, DevicePlugNumber, WhatsPluggedIn, SensorID FROM DeviceSensors WHERE RecordStatus='A'"""
	devices = getCursor().execute(command).fetchall()
	deviceActivationList = []
	for device in devices:
		deviceID = device[0]
		devicePlugNumber = device[1]
		label = device[2]
		transmissions = getDeviceAtDate(deviceID, date)
		index = 0
		startTime = [None]
		endTime = [None]
		time = None
		for transmission in transmissions:
			time = transmission[6]
			if transmission[devicePlugNumber] > 0 and not startTime[index]:
				startTime[index] = time
				startTime.append(None)
			elif transmission[devicePlugNumber] <= 0 and not endTime[index]:
				endTime[index] = time
				endTime.append(None)
				index += 1

		if startTime[index] and not endTime[index]:
			endTime[index] = time
			index += 1

		for i in range(index):
			deviceActivationList.append([label, startTime[i], endTime[i]])

	#print(deviceActivationList)
	return deviceActivationList

def getDeviceAtDate(deviceID, date):
	date = date.strftime('%Y-%m-%d')
	command = """SELECT DeviceID, WattsOutlet1, WattsOutlet2, WattsOutlet3, WattsOutlet4, WattsOutlet5, RxTimeStamp 
				FROM DeviceTransmissions 
				WHERE Convert(date, RxTimeStamp)=Convert(date, '{}') 
				AND DeviceID={}
				ORDER BY RxTimeStamp ASC""".format(date, deviceID)

	transmissions = getCursor().execute(command).fetchall()
	return transmissions

def getLocationAtDate(locationID, date):
	pass
