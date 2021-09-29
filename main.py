import time
from WeatherParser import WeatherParser
from WeatherPreprocessor import WeatherPreprocessor


if __name__ == "__main__":

    parser = WeatherParser(
        station_ids=[34880, 34214],
        start_date="31.12.2018",
        end_date="01.09.2021",
    )
    parser.get_weather_files()
    time.sleep(1)

    preprocessor = WeatherPreprocessor(
        parser=parser,
        merge_type='weeks',
        save_path='/Users/polinariabar/Downloads/',
        downloads_path='/Users/polinariabar/Downloads/',
        dates_list_path='/Users/polinariabar/DS/RP5_weather_parcer/data/dates.xlsx'
    )
    preprocessor.create_unit_file()
    preprocessor.final_day_df.to_excel('/Users/polinariabar/Weather_Test_Day.xlsx', index=False)
    preprocessor.final_week_df.to_excel('/Users/polinariabar/Weather_Test_Week.xlsx', index=False)
