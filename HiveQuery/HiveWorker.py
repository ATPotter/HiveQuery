import xml.etree.ElementTree as ET
import requests
import json
from datetime import datetime

class Worker(object):
    """Class that knows how to interact with the Hive object"""
    
    _urlBase = "https://api-prod.bgchprod.info:443/omnia/{}"

    # RESTful API cndpoints
    _urlCreateSession = "auth/sessions"
    _urlGetDeviceList = "nodes"

    # Headers
    _headers = {
        "Content-Type": "application/vnd.alertme.zoo-6.1+json",
        "Accept": "application/vnd.alertme.zoo-6.1+json",
        "X-Omnia-Client": "Hive Web Dashboard"
        }

    _headerOmniaAccessTokenFormat = "X-Omnia-Access-Token: {}"


    def __init__(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()

        for element in root.findall("username"):
            self.username = element.text

        for element in root.findall("password"):
            self.password = element.text

    # Obtain a session key
    #
    def login(self):
        url = self._urlBase.format(self._urlCreateSession)
        payload = {'sessions': [{
            'username': self.username,
            'password': self.password,
            'caller': 'WEB'}]}

        r = requests.post(url, data=json.dumps(payload), headers=self._headers)

        if(r.status_code < 200) or (r.status_code >= 300):
            print ("Error {} trying to login".format(r.status_code))
            raise
        else:
            response = r.json()

            self.sessionId = response['sessions'][0]['sessionId']

            # Add the session ID to the headers
            self._headers["X-Omnia-Access-Token"] = self.sessionId

    def getTemperatureData(self):

        # If we haven't got a session ID, get one
        #
        if 'X-Omnia-Access-Token' not in self._headers:
            self.login()

        if  'X-Omnia-Access-Token' not in self._headers:
            raise NameError("Login failed")

        url = self._urlBase.format(self._urlGetDeviceList)

        r = requests.get(url, headers=self._headers)

        if(r.status_code < 200) or (r.status_code >= 300):
            print ("Error {} trying to get device status".format(r.status_code))
            return {}

        foundTemperatureData = False
        temperatureValue = 0.0
        temperatureReportedTime = 0

        foundTargetTemperatureData = False
        targetTemperatureValue = 0.0
        targetTemperatureReportedTime = 0


        foundBatteryState = False
        batteryState = ''

        json_data = json.loads(r.text)

        nodes = json_data['nodes']

        for el in nodes:
            if('name' in el) and (el['name'] == 'Thermostat 1'):

                # There are two nodes with Thermostat 1, one for temperature and
                # one for battery (and other) information
                #

                # Look for the actual temperature
                #
                if('attributes' in el) and ('temperature' in el['attributes']):

                    temperatureNode = el['attributes']['temperature']

                    if ('reportedValue' in temperatureNode) and ('reportReceivedTime' in temperatureNode):
                        try:
                            temperatureValue = float(temperatureNode['reportedValue'])
                            temperatureReportedTime = int(int(temperatureNode['reportReceivedTime']) / 1000)
                            foundTemperatureData = True

                        except:
                            foundTemperatureData = False

                # Now look for the target temperature
                #
                if('attributes' in el) and ('targetHeatTemperature' in el['attributes']):

                    targetTemperatureNode =  el['attributes']['targetHeatTemperature']

                    if ('reportedValue' in temperatureNode) and ('reportReceivedTime' in temperatureNode):

                        try:
                            targetTemperatureValue = float(targetTemperatureNode['reportedValue'])
                            targetTemperatureReportedTime = int(int(targetTemperatureNode['reportReceivedTime']) / 1000)
                            foundTargetTemperatureData = True

                        except:
                            foundTargetTemperatureData = True



                if('attributes' in el) and ('batteryState' in el['attributes']):
                    batteryStateNode = el['attributes']['batteryState']

                    if 'reportedValue' in batteryStateNode:
                        batteryState = batteryStateNode['reportedValue']
                        foundBatteryState = True


        return {'foundTemperatureData' : foundTemperatureData,
                'temperatureValue' : temperatureValue,
                'temperatureReportedTime' : temperatureReportedTime,
                'foundTargetTemperatureData' : foundTargetTemperatureData,
                'targetTemperatureValue' : targetTemperatureValue,
                'targetTemperatureReportedTime' : targetTemperatureReportedTime,
                'foundBatteryState' : foundBatteryState,
                'batteryState' : batteryState }

