import pynput.mouse
from pynput.mouse import Button, Listener, Controller
import time
import fastf1
import re
import pandas as pd
import random
# import FastF1_testing

# Converts the default string output from the database into a float that can be worked with
def convert_time(time: str) -> float:
    arr = time.split(':')
    num = 60.00
    num += float(arr[1])
    return num

def is_rain(session) -> bool:
    if "True" in str(session.weather_data['Rainfall']):
        return True
    else:
        return False
    
    # Returns the number fo years since a reg change for known time periods, otherwise returns random reasonable value
def get_years_since_reg_change(year: int) -> int:
    if year > 2030:
        return random.randint(0, 5)
    elif 2026 <= year <= 2030:
        return year - 2026
    elif 2022 <= year <= 2025:
        return year - 2022
    elif 2017 <= year <= 2021:
        return year - 2017
    elif 2014 <= year <= 2016:
        return year - 2014
    elif 2010 <= year <= 2013:
        return year - 2010
    else:
        return random.randint(0, 5)
    
average_grid_positions = { # indexed based on order in the 2024 calendar (Bahrain, Jeddah, ... Abu Dhabi + additionals now (any circuit from 2018 - 2024))
    "VER": {"Bahrain": 5.64, "Jeddah": 5.75, "Australia": 4.13, "Suzuka": 4.38, "China": 8.17, "Miami": 4.33, "Imola": 2.0, "Monaco": 7.78, "Canada": 5.63, "Spain": 3.4, "Austria": 2.92, "Silverstone": 4.0, "Hungary": 5.1, "Spa-Francorchamps": 7.2, "Zandvoort": 1.0, "Monza": 8.78, "Baku": 4.43, "Singapore": 5.57, "Austin": 7.25, "Mexico": 3.25, "Brazil": 3.63, "Las Vegas": 2.0, "Qatar": 4.0, "Abu Dhabi": 3.89, "France": 2.75, "Hockenheim": 3.33, "Russia": 10.71, "Turkey": 2.0, "Portugal": 3.0, "Nürburgring": 3.0},
    "PER": {"Bahrain": 9.21, "Jeddah": 2.5, "Australia": 12.5, "Suzuka": 8.5, "China": 10.0, "Miami": 3.0, "Imola": 6.75, "Monaco": 11.17, "Canada": 12.27, "Spain": 10.0, "Austria": 10.54, "Silverstone": 12.31, "Hungary": 11.57, "Spa-Francorchamps": 6.38, "Zandvoort": 10.67, "Monza": 10.15, "Baku": 5.29, "Singapore": 12.09, "Austin": 9.91, "Mexico": 8.38, "Brazil": 11.25, "Las Vegas": 11.0, "Qatar": 15.5, "Abu Dhabi": 9.15, "France": 8.5, "Hockenheim": 10.8, "Russia": 8.13, "Turkey": 8.0, "Portugal": 4.5, "Nürburgring": 12.33},
    "HAM": {"Bahrain": 3.94, "Jeddah": 7.75, "Australia": 4.06, "Suzuka": 4.14, "China": 5.5, "Miami": 9.0, "Imola": 6.25, "Monaco": 5.47, "Canada": 2.47, "Spain": 4.33, "Austria": 4.23, "Silverstone": 4.05, "Hungary": 3.5, "Spa-Francorchamps": 4.0, "Zandvoort": 6.33, "Monza": 4.65, "Baku": 4.14, "Singapore": 2.93, "Austin": 2.45, "Mexico": 2.88, "Brazil": 5.19, "Las Vegas": 10.0, "Qatar": 2.0, "Abu Dhabi": 2.67, "France": 2.0, "Hockenheim": 7.29, "Russia": 3.25, "Turkey": 6.29, "Portugal": 1.5, "Nürburgring": 4.0},
    "RUS": {"Bahrain": 9.71, "Jeddah": 7.5, "Australia": 8.5, "Suzuka": 10.75, "China": 12.5, "Miami": 8.33, "Imola": 10.5, "Monaco": 10.6, "Canada": 7.75, "Spain": 12.0, "Austria": 10.5, "Silverstone": 11.5, "Hungary": 13.33, "Spa-Francorchamps": 8.33, "Zandvoort": 6.67, "Monza": 10.6, "Baku": 11.75, "Singapore": 13.33, "Austin": 11.75, "Mexico": 11.25, "Brazil": 11.0, "Las Vegas": 3.0, "Qatar": 8.5, "Abu Dhabi": 12.2, "France": 13.33, "Hockenheim": 17.0, "Russia": 11.0, "Turkey": 16.5, "Portugal": 12.5, "Nürburgring": 17},
    "LEC": {"Bahrain": 5.75, "Jeddah": 5.0, "Australia": 7.0, "Suzuka": 5.2, "China": 9.67, "Miami": 3.33, "Imola": 4.0, "Monaco": 6.33, "Canada": 11.2, "Spain": 8.14, "Austria": 7.56, "Silverstone": 5.75, "Hungary": 6.86, "Spa-Francorchamps": 7.43, "Zandvoort": 5.33, "Monza": 6.33, "Baku": 4.8, "Singapore": 4.5, "Austin": 6.0, "Mexico": 5.2, "Brazil": 6.8, "Las Vegas": 1.0, "Qatar": 9.0, "Abu Dhabi": 5.83, "France": 4.75, "Hockenheim": 9.5, "Russia": 9.25, "Turkey": 7.5, "Portugal": 6.0, "Nürburgring": 4.0},
    "SAI": {"Bahrain": 8.64, "Jeddah": 7.33, "Australia": 8.13, "Suzuka": 9.5, "China": 10.5, "Miami": 2.67, "Imola": 7.25, "Monaco": 6.89, "Canada": 11.25, "Spain": 7.0, "Austria": 9.0, "Silverstone": 9.0, "Hungary": 8.1, "Spa-Francorchamps": 10.1, "Zandvoort": 5.0, "Monza": 9.89, "Baku": 9.14, "Singapore": 7.71, "Austin": 8.13, "Mexico": 7.13, "Brazil": 10.63, "Las Vegas": 12.0, "Qatar": 8.5, "Abu Dhabi": 10.33, "France": 9.25, "Hockenheim": 10.0, "Russia": 9.86, "Turkey": 17.0, "Portugal": 6.0, "Nürburgring": 10.0},
    "NOR": {"Bahrain": 10.71, "Jeddah": 10.75, "Australia": 7.0, "Suzuka": 6.0, "China": 9.5, "Miami": 5.0, "Imola": 5.75, "Monaco": 7.2, "Canada": 8.0, "Spain": 7.0, "Austria": 4.75, "Silverstone": 5.57, "Hungary": 4.83, "Spa-Francorchamps": 10.67, "Zandvoort": 7.33, "Monza": 7.4, "Baku": 8.5, "Singapore": 6.33, "Austin": 5.75, "Mexico": 12.75, "Brazil": 6.75, "Las Vegas": 15.0, "Qatar": 7.0, "Abu Dhabi": 5.0, "France": 6.0, "Hockenheim": 19.0, "Russia": 5.33, "Turkey": 10.5, "Portugal": 7.5, "Nürburgring": 8.0},
    "PIA": {"Bahrain": 13.0, "Jeddah": 6.5, "Australia": 10.5, "Suzuka": 4.0, "China": 5.0, "Miami": 12.5, "Imola": 5.0, "Monaco": 6.5, "Canada": 6.0, "Spain": 9.0, "Austria": 10.0, "Silverstone": 4.0, "Hungary": 3.0, "Spa-Francorchamps": 5.0, "Zandvoort": 8.0, "Monza": 7.0, "Baku": 10.0, "Singapore": 17.0, "Austin": 10.0, "Mexico": 7.0, "Brazil": 10.0, "Las Vegas": 18.0, "Qatar": 6.0, "Abu Dhabi": 3.0, "France": 7.94, "Hockenheim": 7.94, "Russia": 7.94, "Turkey": 7.94, "Portugal": 7.94, "Nürburgring": 7.94},
    "ALO": {"Bahrain": 8.0, "Jeddah": 6.5, "Australia": 8.42, "Suzuka": 10.33, "China": 6.31, "Miami": 9.33, "Imola": 10.38, "Monaco": 8.1, "Canada": 6.37, "Spain": 7.29, "Austria": 14.08, "Silverstone": 9.05, "Hungary": 7.29, "Spa-Francorchamps": 9.63, "Zandvoort": 9.0, "Monza": 9.35, "Baku": 11.33, "Singapore": 7.31, "Austin": 11.3, "Mexico": 13.29, "Brazil": 8.8, "Las Vegas": 9.0, "Qatar": 3.5, "Abu Dhabi": 9.69, "France": 10.67, "Hockenheim": 7.55, "Russia": 12.83, "Turkey": 5.88, "Portugal": 13.0, "Nürburgring": 7.56},
    "STR": {"Bahrain": 13.56, "Jeddah": 11.5, "Australia": 13.83, "Suzuka": 15.33, "China": 13.75, "Miami": 13.0, "Imola": 13.25, "Monaco": 15.57, "Canada": 15.33, "Spain": 13.0, "Austria": 11.9, "Silverstone": 13.11, "Hungary": 13.25, "Spa-Francorchamps": 13.63, "Zandvoort": 11.0, "Monza": 10.0, "Baku": 13.0, "Singapore": 17.0, "Austin": 13.67, "Mexico": 17.33, "Brazil": 14.0, "Las Vegas": 19.0, "Qatar": 14.0, "Abu Dhabi": 13.57, "France": 17.5, "Hockenheim": 16.0, "Russia": 11.6, "Turkey": 4.5, "Portugal": 14.5, "Nürburgring": 13.56},
    "RIC": {"Bahrain": 8.69, "Jeddah": 13.0, "Australia": 10.0, "Suzuka": 11.36, "China": 7.22, "Miami": 17.0, "Imola": 6.5, "Monaco": 7.73, "Canada": 7.4, "Spain": 9.5, "Austria": 9.75, "Silverstone": 10.21, "Hungary": 10.71, "Spa-Francorchamps": 10.29, "Zandvoort": 13.5, "Monza": 10.92, "Baku": 8.5, "Singapore": 9.9, "Austin": 8.27, "Mexico": 7.63, "Brazil": 12.75, "Las Vegas": 14.0, "Qatar": 14.0, "Abu Dhabi": 10.62, "France": 8.0, "Hockenheim": 10.2, "Russia": 8.0, "Turkey": 12.5, "Portugal": 13.0, "Nürburgring": 11.33},
    "TSU": {"Bahrain": 13.5, "Jeddah": 13.0, "Australia": 11.0, "Suzuka": 10.67, "China": 19.0, "Miami": 12.0, "Imola": 13.0, "Monaco": 11.0, "Canada": 15.67, "Spain": 15.25, "Austria": 12.8, "Silverstone": 14.5, "Hungary": 14.75, "Spa-Francorchamps": 16.75, "Zandvoort": 13.33, "Monza": 15.33, "Baku": 7.67, "Singapore": 12.5, "Austin": 13.33, "Mexico": 16.0, "Brazil": 17.0, "Las Vegas": 20.0, "Qatar": 9.5, "Abu Dhabi": 8.33, "France": 14.0, "Hockenheim": 13.31, "Russia": 12.0, "Turkey": 9.0, "Portugal": 14.0, "Nürburgring": 13.31},
    "HUL": {"Bahrain": 11.25, "Jeddah": 14.0, "Australia": 10.91, "Suzuka": 12.55, "China": 11.0, "Miami": 10.5, "Imola": 10.0, "Monaco": 11.64, "Canada": 9.73, "Spain": 13.45, "Austria": 8.75, "Silverstone": 9.31, "Hungary": 10.73, "Spa-Francorchamps": 12.73, "Zandvoort": 14.0, "Monza": 11.9, "Baku": 14.8, "Singapore": 10.5, "Austin": 10.0, "Mexico": 8.83, "Brazil": 8.6, "Las Vegas": 13.0, "Qatar": 14.0, "Abu Dhabi": 9.0, "France": 12.5, "Hockenheim": 7.83, "Russia": 10.33, "Turkey": 17.0, "Portugal": 10.8, "Nürburgring": 15.0},
    "MAG": {"Bahrain": 13.4, "Jeddah": 12.0, "Australia": 12.0, "Suzuka": 14.63, "China": 13.5, "Miami": 12.67, "Imola": 14.33, "Monaco": 13.63, "Canada": 14.38, "Spain": 12.44, "Austria": 12.5, "Silverstone": 14.4, "Hungary": 15.67, "Spa-Francorchamps": 12.56, "Zandvoort": 19.0, "Monza": 13.38, "Baku": 15.5, "Singapore": 12.0, "Austin": 13.71, "Mexico": 16.0, "Brazil": 11.0, "Las Vegas": 8.0, "Qatar": 18.0, "Abu Dhabi": 15.13, "France": 14.67, "Hockenheim": 9.25, "Russia": 12.83, "Turkey": 13.0, "Portugal": 19.0, "Nürburgring": 15.0},
    "GAS": {"Bahrain": 11.25, "Jeddah": 10.5, "Australia": 14.8, "Suzuka": 13.17, "China": 12.67, "Miami": 8.0, "Imola": 10.25, "Monaco": 9.67, "Canada": 13.8, "Spain": 10.14, "Austria": 9.67, "Silverstone": 11.0, "Hungary": 11.71, "Spa-Francorchamps": 10.43, "Zandvoort": 9.0, "Monza": 13.0, "Baku": 12.8, "Singapore": 11.25, "Austin": 11.0, "Mexico": 13.33, "Brazil": 11.0, "Las Vegas": 4.0, "Qatar": 4.5, "Abu Dhabi": 13.29, "France": 10.75, "Hockenheim": 12.0, "Russia": 13.25, "Turkey": 11.5, "Portugal": 9.0, "Nürburgring": 12.0},
    "OCO": {"Bahrain": 11.88, "Jeddah": 9.25, "Australia": 12.2, "Suzuka": 11.67, "China": 14.0, "Miami": 13.67, "Imola": 12.25, "Monaco": 9.33, "Canada": 9.6, "Spain": 9.86, "Austria": 11.22, "Silverstone": 11.88, "Hungary": 12.29, "Spa-Francorchamps": 10.25, "Zandvoort": 12.0, "Monza": 12.71, "Baku": 11.6, "Singapore": 13.8, "Austin": 12.17, "Mexico": 13.5, "Brazil": 14.67, "Las Vegas": 16.0, "Qatar": 8.5, "Abu Dhabi": 11.0, "France": 10.67, "Hockenheim": 15.0, "Russia": 8.0, "Turkey": 9.5, "Portugal": 8.5, "Nürburgring": 7.0},
    "ALB": {"Bahrain": 11.67, "Jeddah": 15.0, "Australia": 13.25, "Suzuka": 12.25, "China": 17.0, "Miami": 14.33, "Imola": 12.67, "Monaco": 12.0, "Canada": 11.0, "Spain": 14.6, "Austria": 11.5, "Silverstone": 10.5, "Hungary": 14.2, "Spa-Francorchamps": 10.6, "Zandvoort": 9.5, "Monza": 7.67, "Baku": 13.33, "Singapore": 12.67, "Austin": 9.67, "Mexico": 12.0, "Brazil": 12.33, "Las Vegas": 5.0, "Qatar": 13.0, "Abu Dhabi": 10.75, "France": 12.0, "Hockenheim": 16.0, "Russia": 17.5, "Turkey": 4.0, "Portugal": 6.0, "Nürburgring": 5.0},
    "SAR": {"Bahrain": 17.6, "Jeddah": 19.5, "Australia": 18.0, "Suzuka": 19.5, "China": 20.0, "Miami": 18.5, "Imola": 19.0, "Monaco": 15.5, "Canada": 15.5, "Spain": 19.5, "Austria": 18.5, "Silverstone": 13.0, "Hungary": 17.0, "Spa-Francorchamps": 18.0, "Zandvoort": 10.0, "Monza": 15.0, "Baku": 14.0, "Singapore": 18.0, "Austin": 16.0, "Mexico": 19.0, "Brazil": 19.0, "Las Vegas": 6.0, "Qatar": 15.0, "Abu Dhabi": 20.0, "France": 16.91, "Hockenheim": 16.91, "Russia": 16.91, "Turkey": 16.91, "Portugal": 16.91, "Nürburgring": 16.91},
    "BOT": {"Bahrain": 5.92, "Jeddah": 10.0, "Australia": 12.33, "Suzuka": 8.2, "China": 6.25, "Miami": 10.33, "Imola": 8.0, "Monaco": 10.0, "Canada": 7.3, "Spain": 6.42, "Austria": 6.69, "Silverstone": 8.31, "Hungary": 6.08, "Spa-Francorchamps": 9.67, "Zandvoort": 12.33, "Monza": 8.45, "Baku": 7.43, "Singapore": 9.67, "Austin": 7.2, "Mexico": 5.63, "Brazil": 7.6, "Las Vegas": 7.0, "Qatar": 7.5, "Abu Dhabi": 9.27, "France": 4.5, "Hockenheim": 3.5, "Russia": 4.38, "Turkey": 5.0, "Portugal": 1.5, "Nürburgring": 9.0},
    "ZHO": {"Bahrain": 15.0, "Jeddah": 14.33, "Australia": 16.67, "Suzuka": 17.67, "China": 16.0, "Miami": 16.67, "Imola": 18.5, "Monaco": 19.0, "Canada": 16.67, "Spain": 14.33, "Austria": 16.67, "Silverstone": 13.33, "Hungary": 11.67, "Spa-Francorchamps": 18.0, "Zandvoort": 14.5, "Monza": 12.5, "Baku": 14.5, "Singapore": 16.5, "Austin": 15.0, "Mexico": 11.0, "Brazil": 16.5, "Las Vegas": 17.0, "Qatar": 19.0, "Abu Dhabi": 17.0, "France": 16.0, "Hockenheim": 15.69, "Russia": 15.69, "Turkey": 15.69, "Portugal": 15.69, "Nürburgring": 15.69}
}

track_list = {
    "Bahrain": 90.021,
    "Jeddah": 88.584,
    "Australia": 77.014,
    "Suzuka": 89.285,
    "China": 94.837,
    "Miami": 88.051,
    "Imola": 75.737,
    "Monaco": 71.266,
    "Canada": 72.705,
    "Spain": 72.256,
    "Austria": 65.288,
    "Silverstone": 88.924,
    "Hungary": 76.498,
    "Spa-Francorchamps": 106.075,
    "Zandvoort": 76.690, # from zandvoort onwards should subtract 0.5-1s for 2024 cars
    "Monza": 81.451,
    "Baku": 102.465,
    "Singapore": 92.076,
    "Austin": 95.585,
    "Mexico": 78.306,
    "Brazil": 70.513,
    "Las Vegas": 93.913,
    "Qatar": 85.297,
    "Abu Dhabi": 84.216,
    "France": 92.600, # have to get other data for these 6 tracks
    "Hockenheim": 72.905,
    "Russia": 93.247,
    "Turkey": 84.727,
    "Portugal": 79.244,
    "Nürburgring": 86.637
}

lap_data = { # will be accessed something like (lap_data['driver'][i] = whatever bullshit)
    'driver': [],
    'track': [],
    'year': [],
    'avg_grid_pos_track': [],
    'track_avg_lap_time': [],
    'temperature': [], # higher temp == slower laps (significant, from tire deg and lower engine RPM)
    'rain': [],
    'target_time': [], # just get the actual times basically
    'years_since_reg_change': []
}

session = fastf1.get_session(2017, "Monaco", "Q")
session.load()

track = 'Monaco'

drivers = pd.unique(session.laps['Driver'])

for k in range(len(drivers)):

    # Skip entry if driver is not one of the current 20 drivers
    if drivers[k] not in average_grid_positions.keys():
        continue

    # new code (using more data and different data structure)
    lap_data['driver'].append(drivers[k]) # get driver
    lap_data['track'].append(track) # get track name - figure out how
    lap_data['year'].append(re.findall(r'\d{4}', str(session.date))[0]) # get the year
    lap_data['avg_grid_pos_track'].append(average_grid_positions[drivers[k]][track]) # get the current driver's avg grid position for the given track
    lap_data["track_avg_lap_time"].append(track_list[track]) # find the average lap time for the track (can do avg for one session or try and do historical avg - hist would be less accurate to current cars)
    lap_data['temperature'].append(float(session.weather_data['TrackTemp'][0])) # see how this outputs (if it's even correct)
    lap_data['rain'].append(is_rain(session))
    lap_data["years_since_reg_change"].append(get_years_since_reg_change(2024))

    try:
        if str(session.laps.pick_drivers(drivers[k]).pick_fastest()['LapTime']).__contains__("nan"):
            lap_data["target_time"].append(None)
        else:
            lap_data["target_time"].append(convert_time(re.findall(r'\d{2}\:\d{2}\.\d{3}', str(session.laps.pick_drivers(drivers[k]).pick_fastest()['LapTime']))[0])) # what we're predicting (eq. to y in pytorch examples, will compare predicted time to this for model testing)
    except:
        try:
            if re.findall(r'\d{2}\:\d{2}', str(session.laps.pick_driver(drivers[k]).pick_fastest()['LapTime'])):
                lap_data["target_time"].append(convert_time(re.findall(r'(01:\d{2})', str(session.laps.pick_drivers(drivers[k]).pick_fastest()['LapTime']))[0] + '.000'))
        except:
            lap_data["target_time"].append(None)

for key in lap_data:
    print(lap_data[key])

data = pd.DataFrame.from_dict(lap_data)
data = data.dropna(subset=['target_time'])
data.to_csv('new_race.csv')

# for i in range(20):
#     print(str(session.laps.pick_drivers(drivers[i]).pick_fastest()['LapTime']))
#     print(str(session.laps.pick_drivers(drivers[i]).pick_fastest()['LapTime']).__contains__('nan'))


# Code for getting avg lap time
# avg_time = 0.0
# num = 20
# for i in range(20):
#     try:
#         avg_time += convert_time(re.findall(r'\d{2}\:\d{2}\.\d{3}', str(session.laps.pick_drivers(drivers[i]).pick_fastest()['LapTime']))[0])
#     except:
#         try:
#             avg_time += convert_time(re.findall(r'(01:\d{2})', str(session.laps.pick_drivers(drivers[i]).pick_fastest()['LapTime']))[0] + ".000")
#         except:
#             num -= 1
#             continue

# avg_time /= num
# print(avg_time)


#################################
### TEST THE is_rain FUNCTION ###
#################################


# print(is_rain(session))

# print(session.laps.pick_drivers("HAM").pick_fastest()['LapTime'])
