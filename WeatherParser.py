from GoogleChromeDriver import GoogleChromeDriver
from StationWeather import StationWeather


class WeatherParser:

    def __init__(self, station_ids, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.driver = GoogleChromeDriver()
        self.stations = [StationWeather(st_id, start_date, end_date, self.driver) for st_id in station_ids]
        self.filenames = []
        self.error_stations = []

    def get_weather_files(self):
        print('\n\nDownloading files...')
        self.error_stations = self.get_weather_files_cycle(self.stations)
        if len(self.error_stations) != 0:
            self.error_stations = self.get_weather_files_cycle(self.error_stations)
        if len(self.error_stations) != 0:
            print('\n\nError! This program is unable to download some stations weather archives:')
            print([station.id for station in self.error_stations])

    def get_weather_files_cycle(self, stations):
        error_stations = []
        for station in stations:
            if station.request() and station.download():
                self.filenames.append(station.filename)
            else:
                error_stations.append(station)
        return error_stations
