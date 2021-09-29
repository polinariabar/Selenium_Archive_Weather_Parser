from GoogleChromeDriver import GoogleChromeDriver
import time





class StationWeather:

    def __init__(self, station_id: int, start_date, end_date, driver: GoogleChromeDriver):
        self.id = station_id
        self.start_date = start_date
        self.end_date = end_date
        self.driver = driver
        self.filename = ""

    def request(self):
        self.driver.fill_in_station(self.id)
        times = 0
        done = False
        while times < 5 and done is False:
            times += 1
            try:
                self.driver.choose_station()
                self.driver.change_start_date(self.start_date)
                self.driver.change_end_date(self.end_date)
                self.driver.create_archive()
                done = True
            except:
                time.sleep(1)
        if done is False:
            print("ERROR: There is no such station:", self.id)
        return done

    def download(self):
        times = 0
        done = False
        while times < 5 and done is False:
            try:
                self.filename = self.driver.download_archive()
                print("Station", self.id, "done!")
                done = True
            except:
                time.sleep(1)
        if done is False:
            print("ERROR: Can not download such station:", self.id)
        return done


