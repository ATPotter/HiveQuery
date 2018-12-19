import HiveWorker










def run():
    worker = HiveWorker.Worker("AccountInformation.xml")

    thermostat_info = worker.getTemperatureData()
    

    return




if __name__ == "__main__":
    run()
    exit

