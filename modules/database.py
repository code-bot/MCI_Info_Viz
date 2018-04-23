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

def getAllActivities(sensors,locations,activities,sensorDictList,locDictList):
    activityDictList = []
    #get the specified sensor and location data for an activity
    index = 0
    for activity in activities:
        print(sensors)
        sensor = sensors[index]
        location = locations[index]
        newSensorList = []
        newLocList = []
        for sensorDict in sensorDictList:
            if sensor == sensorDict['sensor']:
                newSensorList.append(sensorDict)
        for locDict in locDictList:
            if location == locDict['location']:
                newLocList.append(locDict)
        #get start and end times
        times = getActivityTimes(newSensorList,newLocList)
        for time in times:
            actDict = {}
            actDict['activity'] = activity
            actDict['startTime'] = time[0]
            actDict['endTime'] = time[1]
            actDict['location'] = location
            activityDictList.append(actDict)
        index += 1
    print(activityDictList)
    return activityDictList
#          {
#            "activity": "sleeping",
#            "startTime": "Sat Apr 14 2018 00:00:00 GMT-0500 (EST)",
#            "endTime": "Sat Apr 14 2018 07:30:00 GMT-0500 (EST)",
#            "location": "bedroom"
#          },
#          {
#            "activity": "cooking",
#            "startTime": "Sat Apr 14 2018 08:15:00 GMT-0500 (EST)",
#            "endTime": "Sat Apr 14 2018 10:30:00 GMT-0500 (EST)",
#            "location": "kitchen"
#          },
#          {
#            "activity": "entertainment",
#            "startTime": "Sat Apr 14 2018 10:35:00 GMT-0500 (EST)",
#            "endTime": "Sat Apr 14 2018 13:00:00 GMT-0500 (EST)",
#            "location": "living"
#          },
#          {
#            "activity": "cooking",
#            "startTime": "Sat Apr 14 2018 17:00:00 GMT-0500 (EST)",
#            "endTime": "Sat Apr 14 2018 18:00:00 GMT-0500 (EST)",
#            "location": "kitchen"
#          },
#          {
#            "activity": "entertainment",
#            "startTime": "Sat Apr 14 2018 18:15:00 GMT-0500 (EST)",
#            "endTime": "Sat Apr 14 2018 20:30:00 GMT-0500 (EST)",
#            "location": "kitchen"
#          },
#          {
#            "activity": "sleeping",
#            "startTime": "Sat Apr 14 2018 21:00:00 GMT-0500 (EST)",
#            "endTime": "Sat Apr 14 2018 23:00:00 GMT-0500 (EST)",
#            "location": "bedroom"
#          }
#        ]

def getActivityTimes(sensorDictList, locationDictList):
    activityTimes = []
    for sensorDict in sensorDictList:
        for locDict in locationDictList:
            if sensorDict['startTime'] <= locDict['endTime'] and sensorDict['startTime'] >= locDict['startTime']:
                if sensorDict['endTime'] <= locDict['endTime'] and sensorDict['endTime'] >= locDict['startTime']:
                    activityTimes.append([sensorDict['startTime'],sensorDict['endTime']])
                elif locDict['endTime'] <= sensorDict['endTime'] and locDict['endTime'] >= sensorDict['endTime']:
                    activityTimes.append([sensorDict['startTime'],locDict['endTime']])
            elif locDict['startTime'] <= sensorDict['endTime'] and locDict['startTime'] >= sensorDict['startTime']:
                if locDict['endTime'] <= sensorDict['endTime'] and locDict['endTime'] >= sensorDict['endTime']:
                    activityTimes.append([locDict['startTime'],locDict['endTime']])
                elif sensorDict['endTime'] <= locDict['endTime'] and sensorDict['endTime'] >= locDict['startTime']:
                    activityTimes.append([locDict['startTime'],sensorDict['endTime']])

    return activityTimes

def getAllLocationsAtDate(date):
    # locationList = []
    # tagID = 56080 #tag 16
    # command = """SELECT ID, RoomName FROM Rooms"""
    # rooms = getCursor().execute(command).fetchall()
    # for room in rooms:        
    #     index = 0
    #     startTime = [None]
    #     endTime = [None]
    #     time = None
        
    #     transmissions = getLocationAtDate(tagID,date)
        
    #     for j in range(1,len(transmissions)):
    #         transmission = transmissions[j]
    #         time = transmission[1]
    #         currRoom = transmission[0]
    #         prevRoom = transmissions[j-1][0]
    #         if currRoom == room[0] and not startTime[index]:
    #             startTime[index] = time
    #             startTime.append(None)
    #             #print(startTime[index])
    #         elif currRoom != prevRoom and not endTime[index] and startTime[index]:
    #             endTime[index] = time
    #             #print(endTime[index])
    #             endTime.append(None)
    #             index +=1
            
    #     if startTime[index] and not endTime[index]:
    #         endTime[index] = time
    #         index += 1
        
    #     for i in range(index):
    #         #print(endTime[i]-startTime[i])
    #         locationDict = {}
    #         if (endTime[i]-startTime[i])>datetime.timedelta(minutes=1):
    #             locationDict['location'] = room[1]
    #             locationDict['startTime'] = startTime[i].strftime('%Y-%m-%d %H:%M:%S')
    #             locationDict['endTime'] = endTime[i].strftime('%Y-%m-%d %H:%M:%S')
    #             locationList.append(locationDict)
            
    # return locationList
    return [
          {
            "location": "bedroom",
            "startTime": "Sat Apr 14 2018 00:00:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 07:30:00 GMT-0500 (EST)",
          },
          {
            "location": "bathroom",
            "startTime": "Sat Apr 14 2018 07:40:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 08:05:00 GMT-0500 (EST)",
          },
          {
            "location": "kitchen",
            "startTime": "Sat Apr 14 2018 08:15:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 08:45:00 GMT-0500 (EST)",
          },
          {
            "location": "living",
            "startTime": "Sat Apr 14 2018 08:50:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 09:15:00 GMT-0500 (EST)",
          },
          {
            "location": "kitchen",
            "startTime": "Sat Apr 14 2018 09:15:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 10:30:00 GMT-0500 (EST)",
          },
          {
            "location": "living",
            "startTime": "Sat Apr 14 2018 10:35:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 11:45:00 GMT-0500 (EST)",
          },
          {
            "location": "bedroom",
            "startTime": "Sat Apr 14 2018 11:50:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 12:30:00 GMT-0500 (EST)",
          },
          {
            "location": "living",
            "startTime": "Sat Apr 14 2018 12:35:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 13:00:00 GMT-0500 (EST)",
          },
          {
            "location": "kitchen",
            "startTime": "Sat Apr 14 2018 17:00:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 18:00:00 GMT-0500 (EST)",
          },
          {
            "location": "living",
            "startTime": "Sat Apr 14 2018 18:15:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 20:30:00 GMT-0500 (EST)",
          },
          {
            "location": "bathroom",
            "startTime": "Sat Apr 14 2018 20:35:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 21:00:00 GMT-0500 (EST)",
          },
          {
            "location": "bedroom",
            "startTime": "Sat Apr 14 2018 21:00:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 23:00:00 GMT-0500 (EST)",
          }
        ]

def getAllDevicesAtDate(date):
#     deviceList = []
#     command = """SELECT DeviceID, DevicePlugNumber, WhatsPluggedIn, SensorID FROM DeviceSensors WHERE RecordStatus='A'"""
#     devices = getCursor().execute(command).fetchall()
#     #map deviceID+plug to device name (later users can input name into database)
#     deviceMap = {}
#     deviceMap[43536] = {3:'TV',5:'Xbox'}
#     deviceMap[43578] = {4:'stove'}
#     deviceMap[49943] = {4:'toilet'}
#     deviceDict = {}
#     threshold = 20; #set watts threshold so you don't pick up weird stuff
#     for device in devices:
#         deviceID = device[0]
#         devicePlugNumber = device[1]
#         #if device is in device map assign proper label
#         if deviceID in deviceMap.keys():
#             if devicePlugNumber in deviceMap[deviceID].keys():
#                 label = deviceMap[deviceID][devicePlugNumber]
#             else:
#                 label = device[2]
#         else:
#             label = device[2]
#         #print(label)
#         transmissions = getDeviceAtDate(deviceID, date)
        
#         index = 0
#         startTime = [None]
#         endTime = [None]
#         time = None
#         for j in range(1,len(transmissions)):
#             transmission = transmissions[j]
#             watts = transmission[devicePlugNumber]
#             prevWatts = transmissions[j-1][devicePlugNumber]
# #            if deviceID == 43536 and devicePlugNumber == 3:
#                 #print(watts - prevWatts)
#             time = transmission[6]
#             if (watts - prevWatts) > threshold and not startTime[index]:
#                 startTime[index] = time
#                 #print(startTime[index])
#                 startTime.append(None)
#             elif (watts - prevWatts) < -threshold and not endTime[index] and startTime[index]:
#                 endTime[index] = time
#                 #print(endTime[index])
#                 endTime.append(None)
#                 index += 1
        
#         if startTime[index] and not endTime[index]:
#             endTime[index] = time
#             index += 1
        
        
#         for i in range(index):
#             #print(endTime[i]-startTime[i])
#             deviceDict = {}
#             if (endTime[i]-startTime[i])>datetime.timedelta(minutes=4):
#                 deviceDict['sensor'] = label
#                 deviceDict['startTime'] = startTime[i].strftime('%Y-%m-%d %H:%M:%S')
#                 deviceDict['endTime'] = endTime[i].strftime('%Y-%m-%d %H:%M:%S')
#                 deviceList.append(deviceDict)
            #deviceActivationList.append([label, startTime[i], endTime[i]])
    
    #print(deviceActivationList)
    #print(deviceDict.keys())
    # return deviceList
	return [
          {
            "sensor": "stove",
            "startTime": "Sat Apr 14 2018 08:15:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 09:15:00 GMT-0500 (EST)",
            "location": "kitchen"
          },
          {
            "sensor": "microwave",
            "startTime": "Sat Apr 14 2018 09:15:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 09:30:00 GMT-0500 (EST)",
            "location": "kitchen"
          },
          {
            "sensor": "stove",
            "startTime": "Sat Apr 14 2018 09:45:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 10:15:00 GMT-0500 (EST)",
            "location": "kitchen"
          },
          {
            "sensor": "TV",
            "startTime": "Sat Apr 14 2018 10:35:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 13:00:00 GMT-0500 (EST)",
            "location": "living"
          },
          {
            "sensor": "stove",
            "startTime": "Sat Apr 14 2018 17:00:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 18:00:00 GMT-0500 (EST)",
            "location": "kitchen"
          },
          {
            "sensor": "XBox",
            "startTime": "Sat Apr 14 2018 18:15:00 GMT-0500 (EST)",
            "endTime": "Sat Apr 14 2018 20:30:00 GMT-0500 (EST)",
            "location": "living"
          }
        ]

def getDevicesAtAllLocations():
	return {
		'kitchen': ['stove'],
		'living': ['TV', 'XBox'],
		'bathroom': ['toilet']
	}

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
