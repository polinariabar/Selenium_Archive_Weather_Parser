import gzip
import shutil
import pandas as pd
from WeatherParser import WeatherParser


def load_data(path, sheet=None):
    data = pd.read_excel(path, engine='openpyxl', sheet_name=sheet)
    if data[data.columns[0]].isna().any():
        data.drop(data.loc[data[data.columns[0]].isna()].index, inplace=True)
    return data


def week_mean(st_df, day_mean_df, dates_list):
    week_mean_df = pd.DataFrame(columns=st_df.columns)
    station = st_df['Station'][0]
    i = 0
    for week_date in dates_list:
        w_df = day_mean_df[day_mean_df['Date'] == week_date]
        if len(w_df) != 0:
            w_index = w_df.index[0]
            week_mean_df.loc[i, 'Station'] = station
            week_mean_df.loc[i, 'Date'] = week_date
            week_mean_df.loc[i, 'T'] = day_mean_df.loc[w_index:w_index+6, 'T'].mean()
            week_mean_df.loc[i, 'RRR'] = day_mean_df.loc[w_index:w_index+6, 'RRR'].sum()
            i += 1
    return week_mean_df


def day_mean(st_df):
    day_mean_df = pd.DataFrame(columns=st_df.columns)
    station = st_df['Station'][0]
    i = 0
    for measureDate in st_df['Date'].unique():
        day_mean_df.loc[i, 'Station'] = station
        day_mean_df.loc[i, 'Date'] = measureDate
        day_mean_df.loc[i, 'T'] = st_df[st_df['Date'] == measureDate]['T'].mean()
        day_mean_df.loc[i, 'U'] = st_df[st_df['Date'] == measureDate]['U'].mean()
        day_mean_df.loc[i, 'RRR'] = st_df[st_df['Date'] == measureDate]['RRR'].sum()
        i += 1
    return day_mean_df


class WeatherPreprocessor:

    def __init__(self, parser: WeatherParser, merge_type, save_path, downloads_path, dates_list_path):
        self.parser = parser
        self.merge_type = merge_type
        self.save_path = save_path
        self.downloads_path = downloads_path
        self.dates_list = load_data(dates_list_path, 'Data')['Date'].dt.date.values
        self.final_week_df = pd.DataFrame()
        self.final_day_df = pd.DataFrame()

    def unzip_files(self):
        for filename in self.parser.filenames:
            with gzip.open(self.downloads_path + filename, 'rb') as f_in:
                with open(self.save_path + filename[:-3], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        for i in range(len(self.parser.filenames)):
            self.parser.filenames[i] = self.parser.filenames[i][:-3]

    def read_file(self, filename):
        df = pd.read_excel(open(self.save_path + filename, 'rb'), skiprows=6)
        df.columns.values[0] = 'Date'
        station = filename.split('.')[0]
        df.insert(0, 'Station', [station] * len(df))
        df = df.reindex(index=df.index[::-1])
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True).dt.date
        df = df.fillna(0)
        df = df[['Station', 'Date', 'T', 'RRR', 'U']]
        df['RRR'] = df['RRR'].replace(['No precipitation'], 0)
        df['RRR'] = df['RRR'].replace(['Trace of precipitation'], 0.001)
        return df

    def convert_into_weeks(self):
        final_week_df = pd.DataFrame()
        for filename in self.parser.filenames:
            curr_station_df = self.read_file(filename)
            day_mean_df = day_mean(curr_station_df)
            week_mean_df = week_mean(curr_station_df, day_mean_df, self.dates_list)
            final_week_df = final_week_df.append(week_mean_df)
        final_week_df = final_week_df.reset_index()
        del final_week_df['index']
        self.final_week_df = final_week_df

    def convert_into_days(self):
        final_day_df = pd.DataFrame()
        for filename in self.parser.filenames:
            curr_station_df = self.read_file(filename)
            day_mean_df = day_mean(curr_station_df)
            final_day_df = final_day_df.append(day_mean_df)
        final_day_df = final_day_df.reset_index()
        del final_day_df['index']
        self.final_day_df = final_day_df

    def create_unit_file(self):
        print("\n\n Unzipping files...")
        self.unzip_files()
        print("\n\n Creating final file...\n")
        self.convert_into_weeks()
        self.convert_into_days()
