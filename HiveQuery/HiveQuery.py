import HiveWorker
import HiveDbAccess










def run():
    worker = HiveWorker.Worker("AccountInformation.xml")
    database = HiveDbAccess.Worker("DatabaseAccess.xml")

    thermostat_info = worker.getTemperatureData()

    

    return




if __name__ == "__main__":
    run()
    exit

