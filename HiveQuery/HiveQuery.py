import HiveWorker
import HiveDbAccess










def run():
    worker = HiveWorker.Worker("AccountInformation.xml")
    thermostat_info = worker.getTemperatureData()

    database = HiveDbAccess.Worker("DatabaseAccess.xml")
    database.StoreRecord(thermostat_info)

    return




if __name__ == "__main__":
    run()
    exit

