from multiprocessing import Process, Manager, freeze_support
from cleaning import scrape_section
from seperate import seperation


if __name__ == "__main__":
    freeze_support()
    version = 150
    manager = Manager()
    check_stocks = manager.list()
    df1, df2, df3, df4, port1, port2, port3, port4,\
        port5, port6, port7, port8, driver1, driver2, driver3, driver4 = seperation()
    process1 = Process(target=scrape_section, args=(df1, port1, driver1, check_stocks, version, "Driver 1", port5, ))
    process2 = Process(target=scrape_section, args=(df2, port2, driver2, check_stocks, version, "Driver 2", port6, ))
    process3 = Process(target=scrape_section, args=(df3, port3, driver3, check_stocks, version, "Driver 3", port7, ))
    process4 = Process(target=scrape_section, args=(df4, port4, driver4, check_stocks, version, "Driver 4", port8, ))
    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process1.join()
    process2.join()
    process3.join()
    process4.join()

    print("Done Trading for the Day! $$$$")







