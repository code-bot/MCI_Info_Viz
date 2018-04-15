import pyodbc
from config import Config
import datetime

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

def getAllActivities():
	return [
		  {
		    "activity": "cooking",
		    "startTimeActivity": "Fri Feb 07 2013 12:00:00 GMT-0500 (EST)",
		    "endTimeActivity": "Fri Feb 07 2013 13:00:00 GMT-0500 (EST)",
		    "location": "kitchen"
		  },
		  {
		    "activity": "cooking",
		    "startTimeActivity": "Fri Feb 07 2013 11:00:00 GMT-0500 (EST)",
		    "endTimeActivity": "Fri Feb 07 2013 12:00:00 GMT-0500 (EST)",
		    "location": "kitchen"
		  },
		  {
		    "activity": "dancing",
		    "startTimeActivity": "Fri Feb 07 2013 12:00:00 GMT-0500 (EST)",
		    "endTimeActivity": "Fri Feb 07 2013 13:00:00 GMT-0500 (EST)",
		    "location": "living"
		  },
		  {
		    "activity": "cooking",
		    "startTimeActivity": "Fri Feb 07 2013 14:00:00 GMT-0500 (EST)",
		    "endTimeActivity": "Fri Feb 07 2013 15:00:00 GMT-0500 (EST)",
		    "location": "kitchen"
		  },
		  {
		    "activity": "cooking",
		    "startTimeActivity": "Fri Feb 07 2013 15:00:00 GMT-0500 (EST)",
		    "endTimeActivity": "Fri Feb 07 2013 16:30:00 GMT-0500 (EST)",
		    "location": "kitchen"
		  },
		  {
		    "activity": "cooking",
		    "startTimeActivity": "Fri Feb 07 2013 16:00:00 GMT-0500 (EST)",
		    "endTimeActivity": "Fri Feb 07 2013 17:00:00 GMT-0500 (EST)",
		    "location": "kitchen"
		  }
		]

def getActivityTimes(sensor, location, sensorDict, locationDict):
    activityDict = {}
    if sensor == 'Stove' and location == 'The Kitchen':
        #activity = cooking
        activityDict['Cooking'] = []
        for senTimes in sensorDict[sensor]:
            for locTimes in locationDict[location]:
                activityDict['Cooking'] = locTimes
    return activityDict

def getAllLocationsAtDate(date):
    locationList = []
    tagID = 56080 #tag 16
    command = """SELECT ID, RoomName FROM Rooms"""
    rooms = getCursor().execute(command).fetchall()
    for room in rooms:        
        index = 0
        startTime = [None]
        endTime = [None]
        time = None
        
        transmissions = getLocationAtDate(tagID,date)
        
        for j in range(1,len(transmissions)):
            transmission = transmissions[j]
            time = transmission[1]
            currRoom = transmission[0]
            prevRoom = transmissions[j-1][0]
            if currRoom == room[0] and not startTime[index]:
                startTime[index] = time
                startTime.append(None)
                #print(startTime[index])
            elif currRoom != prevRoom and not endTime[index] and startTime[index]:
                endTime[index] = time
                #print(endTime[index])
                endTime.append(None)
                index +=1
            
        if startTime[index] and not endTime[index]:
            endTime[index] = time
            index += 1
        
        for i in range(index):
            #print(endTime[i]-startTime[i])
            locationDict = {}
            if (endTime[i]-startTime[i])>datetime.timedelta(minutes=1):
                    locationDict['location'] = room[1]
                    locationDict['startTime'] = startTime[i]
                    locationDict['endTime'] = endTime[i]
                    locationList.append(locationDict)
            
    return locationList

def getAllDevicesAtDate(date):
    deviceList = []
    command = """SELECT DeviceID, DevicePlugNumber, WhatsPluggedIn, SensorID FROM DeviceSensors WHERE RecordStatus='A'"""
    devices = getCursor().execute(command).fetchall()
    #map deviceID+plug to device name (later users can input name into database)
    deviceMap = {}
    deviceMap[43536] = {3:'TV',5:'Xbox360'}
    deviceMap[43578] = {4:'Stove'}
    deviceMap[49943] = {4:'Toilet'}
    #deviceActivationList = []
    #print(date)
    #print(datetime.datetime.today())
    deviceDict = {}
    threshold = 20; #set watts threshold so you don't pick up weird stuff
    for device in devices:
        deviceID = device[0]
        devicePlugNumber = device[1]
        #if device is in device map assign proper label
        if deviceID in deviceMap.keys():
            if devicePlugNumber in deviceMap[deviceID].keys():
                label = deviceMap[deviceID][devicePlugNumber]
            else:
                continue
        else:
            continue
        #print(label)
        transmissions = getDeviceAtDate(deviceID, date)
        
        index = 0
        startTime = [None]
        endTime = [None]
        time = None
        for j in range(1,len(transmissions)):
            transmission = transmissions[j]
            watts = transmission[devicePlugNumber]
            prevWatts = transmissions[j-1][devicePlugNumber]
#            if deviceID == 43536 and devicePlugNumber == 3:
                #print(watts - prevWatts)
            time = transmission[6]
            if (watts - prevWatts) > threshold and not startTime[index]:
                startTime[index] = time
                #print(startTime[index])
                startTime.append(None)
            elif (watts - prevWatts) < -threshold and not endTime[index] and startTime[index]:
                endTime[index] = time
                #print(endTime[index])
                endTime.append(None)
                index += 1
        
        if startTime[index] and not endTime[index]:
            endTime[index] = time
            index += 1
        
        
        for i in range(index):
            #print(endTime[i]-startTime[i])
            deviceDict = {}
            if (endTime[i]-startTime[i])>datetime.timedelta(minutes=4):
                deviceDict['device'] = label
                deviceDict['startTime'] = startTime[i]
                deviceDict['endTime'] = endTime[i]
                deviceList.append(deviceDict)
            #deviceActivationList.append([label, startTime[i], endTime[i]])
    
    #print(deviceActivationList)
    #print(deviceDict.keys())
    return deviceList
	
#	return [
#		  {
#		    "location": "kitchen",
#		    "startTimeLocation": "Fri Feb 07 2013 12:00:00 GMT-0500 (EST)",
#		    "endTimeLocation": "Fri Feb 07 2013 13:00:00 GMT-0500 (EST)"
#		  },
#		  {
#		    "location": "kitchen",
#		    "startTimeLocation": "Fri Feb 07 2013 11:00:00 GMT-0500 (EST)",
#		    "endTimeLocation": "Fri Feb 07 2013 12:00:00 GMT-0500 (EST)"
#		  },
#		  {
#		    "location": "living",
#		    "startTimeLocation": "Fri Feb 07 2013 12:00:00 GMT-0500 (EST)",
#		    "endTimeLocation": "Fri Feb 07 2013 13:00:00 GMT-0500 (EST)"
#		  },
#		  {
#		    "location": "living",
#		    "startTimeLocation": "Fri Feb 07 2013 14:00:00 GMT-0500 (EST)",
#		    "endTimeLocation": "Fri Feb 07 2013 15:00:00 GMT-0500 (EST)"
#		  },
#		  {
#		    "location": "kitchen",
#		    "startTimeLocation": "Fri Feb 07 2013 15:00:00 GMT-0500 (EST)",
#		    "endTimeLocation": "Fri Feb 07 2013 16:30:00 GMT-0500 (EST)"
#		  },
#		  {
#		    "location": "living",
#		    "startTimeLocation": "Fri Feb 07 2013 16:00:00 GMT-0500 (EST)",
#		    "endTimeLocation": "Fri Feb 07 2013 17:00:00 GMT-0500 (EST)"
#		  }
#		]
#
#
#def getAllDevicesAtDate(date):
#	return [
#		  {
#		    "sensor": "stove",
#		    "startTimeSensor": "Fri Feb 07 2013 08:00:00 GMT-0500 (EST)",
#		    "endTimeSensor": "Fri Feb 07 2013 09:00:00 GMT-0500 (EST)",
#		    "location": "kitchen"
#		  },
#		  {
#		    "sensor": "microwave",
#		    "startTimeSensor": "Fri Feb 07 2013 09:00:00 GMT-0500 (EST)",
#		    "endTimeSensor": "Fri Feb 07 2013 10:00:00 GMT-0500 (EST)",
#		    "location": "kitchen"
#		  },
#		  {
#		    "sensor": "TV",
#		    "startTimeSensor": "Fri Feb 07 2013 10:00:00 GMT-0500 (EST)",
#		    "endTimeSensor": "Fri Feb 07 2013 12:00:00 GMT-0500 (EST)",
#		    "location": "living"
#		  },
#		  {
#		    "sensor": "Xbox",
#		    "startTimeSensor": "Fri Feb 07 2013 12:00:00 GMT-0500 (EST)",
#		    "endTimeSensor": "Fri Feb 07 2013 14:00:00 GMT-0500 (EST)",
#		    "location": "living"
#		  },
#		  {
#		    "sensor": "TV",
#		    "startTimeSensor": "Fri Feb 07 2013 14:00:00 GMT-0500 (EST)",
#		    "endTimeSensor": "Fri Feb 07 2013 15:00:00 GMT-0500 (EST)",
#		    "location": "kitchen"
#		  },
#		  {
#		    "sensor": "stove",
#		    "startTimeSensor": "Fri Feb 07 2013 08:00:00 GMT-0500 (EST)",
#		    "endTimeSensor": "Fri Feb 07 2013 08:30:00 GMT-0500 (EST)",
#		    "location": "kitchen"
#		  },
#		  {
#		    "sensor": "TEST",
#		    "startTimeSensor": "Fri Feb 07 2013 10:00:00 GMT-0500 (EST)",
#		    "endTimeSensor": "Fri Feb 07 2013 12:00:00 GMT-0500 (EST)",
#		    "location": "kitchen"
#		  }
#		]
#
#	command = """SELECT DeviceID, DevicePlugNumber, WhatsPluggedIn, SensorID FROM DeviceSensors WHERE RecordStatus='A'"""
#	devices = getCursor().execute(command).fetchall()
#	deviceActivationList = []
#	for device in devices:
#		deviceID = device[0]
#		devicePlugNumber = device[1]
#		label = device[2]
#		transmissions = getDeviceAtDate(deviceID, date)
#		index = 0
#		startTime = [None]
#		endTime = [None]
#		time = None
#		for transmission in transmissions:
#			time = transmission[6]
#			if transmission[devicePlugNumber] > 0 and not startTime[index]:
#				startTime[index] = time
#				startTime.append(None)
#			elif startTime[index] and transmission[devicePlugNumber] <= 0 and not endTime[index]:
#				endTime[index] = time
#				endTime.append(None)
#				index += 1
#
#		
#		if startTime[index] and index < len(endTime) and not endTime[index]:
#			endTime[index] = time
#			index += 1
#
#		for i in range(index):
#			deviceActivationList.append([label, startTime[i], endTime[i]])
#
#	#print(deviceActivationList)
#	return deviceActivationList

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
    date = date.strftime('%Y-%m-%d')
    command = """SELECT RoomID, EndOfMinuteInterval FROM tbl_PTagCalculatedLocation
              WHERE Convert(date, EndOfMinuteInterval)=Convert(date, '{}') AND PTagID={}
              ORDER BY EndOfMinuteInterval ASC""".format(date,locationID)
    transmissions = getCursor().execute(command).fetchall()
    return transmissions
