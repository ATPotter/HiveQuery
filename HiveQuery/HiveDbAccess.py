import xml.etree.ElementTree as ET

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



        print ("Username: {}".format(self.dbUsername))
        print ("Password: {}".format(self.dbPassword))
        print ("Host:     {}".format(self.dbHost))
        print ("Port:     {}".format(self.dbPort))
        print ("Database: {}".format(self.dbDatabase))

