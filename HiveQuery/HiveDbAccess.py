import xml.etree.ElementTree as ET
import mysql.connector
from datetime import datetime, date

class Worker(object):
    """Allows access to the backend database I am using"""


    def __init__(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()

        for element in root.findall("username"):
            self.dbUsername = element.text

        for element in root.findall("password"):
            self.dbPassword = element.text

        for element in root.findall("host"):
            self.dbHost = element.text

        for element in root.findall("port"):
            self.dbPort = element.text

        for element in root.findall("database"):
            self.dbDatabase = element.text


    def StoreRecord(self, myRecord):
        temperatureValid = myRecord['foundTemperatureData']
        temperatureValue = 0
        timeTemperatureRecorded = 0
        if temperatureValid:
            temperatureValue = myRecord['temperatureValue']
            timeTemperatureRecorded = myRecord['temperatureReportedTime']

        targetTemperatureValid = myRecord['foundTargetTemperatureData']
        targetTemperature = 0
        timeTargetTemperature = 0
        if targetTemperatureValid:
            targetTemperature = myRecord['targetTemperatureValue']
            timeTargetTemperature = myRecord['targetTemperatureReportedTime']

        batteryStateValid = myRecord['foundBatteryState']
        batteryStateValue = ''
        if batteryStateValid:
            batteryStateValue = myRecord['batteryState']


        temperatureTimeString = datetime.utcfromtimestamp(timeTemperatureRecorded).strftime('%Y-%m-%d %H:%M:%S')
        targetTemperatureTimeString = datetime.utcfromtimestamp(timeTargetTemperature).strftime('%Y-%m-%d %H:%M:%S')
        batteryStateTimeString = temperatureTimeString

        timeNow = datetime.utcnow()
        timeNowString = timeNow.strftime('%Y-%m-%d %H:%M:%S')

        try:
            cnx = mysql.connector.connect(
                user = self.dbUsername,
                password = self.dbPassword,
                host = self.dbHost,
                port = self.dbPort,
                database = self.dbDatabase)

            cursor = cnx.cursor()

            # First set up the sample_time record and get the primary key we will be
            # using throughout.
            #
            add_sample_time = "INSERT INTO sample_time (sample_time) VALUES (%s)"
            data_sample_time = (timeNow, )
            cursor.execute(add_sample_time, data_sample_time)

            record_number = cursor.lastrowid

            # Now write the three other tables
            addTemperatureCommand = 'INSERT INTO actual_temperature (sample_number, valid, temperature, acquisition_time) VALUES (%s, %s, %s, %s)'
            actualTemperatureData = (record_number, temperatureValid, temperatureValue, temperatureTimeString)

            addTargetTemperatureCommand = 'INSERT INTO target_temperature (sample_number, valid, temperature, acquisition_time) VALUES (%s, %s, %s, %s)'
            targetTemperatureData = (record_number, targetTemperatureValid, targetTemperature, targetTemperatureTimeString)

            addBatteryStateCommand = 'INSERT INTO battery_state (sample_number, valid, state, acquisition_time) VALUES (%s, %s, %s, %s)'
            batteryStateData = (record_number, batteryStateValid, batteryStateValue, temperatureTimeString)

            cursor.execute(addTemperatureCommand, actualTemperatureData)
            cursor.execute(addTargetTemperatureCommand, targetTemperatureData)
            cursor.execute(addBatteryStateCommand, batteryStateData)

            cnx.commit()
            cursor.close()
            cnx.close()


        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()

        return