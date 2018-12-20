#! /usr/bin/python3

import os
import HiveWorker
import HiveDbAccess










def run(path):

    accountFilename = os.path.join(path, "AccountInformation.xml")
    databaseFilename = os.path.join(path, "DatabaseAccess.xml")


    worker = HiveWorker.Worker(accountFilename)
    thermostat_info = worker.getTemperatureData()

    database = HiveDbAccess.Worker(databaseFilename)
    database.StoreRecord(thermostat_info)

    return




if __name__ == "__main__":
    run(os.path.dirname(os.path.abspath(__file__)))
    exit

