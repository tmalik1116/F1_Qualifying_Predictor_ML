import fastf1
import pandas as pd
import numpy as np
import re
import torch
from torch import nn
import matplotlib.pyplot as plt
import utils


class CustomModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.weights = nn.Parameter(torch.randn(1, dtype=torch.float, requires_grad=True))

        self.bias = nn.Parameter(torch.randn(1, dtype=torch.float, requires_grad=True))

    def forward(self, x: torch.Tensor):
        return self.weights * x + self.bias # y = mx+b (purely linear, not expecting it to work well)


pole_times_2023 = [
    89.708,
    88.265,
    76.732,
    100.203,
    86.814,
    71.365,
    72.272,
    78.725,
    64.391,
    86.720,
    76.609,
    106.168,
    70.567,
    80.294,
    90.984,
    88.877,
    83.778,
    94.723,
    77.166,
    70.021,
    92.726,
    83.445
]

pole_times_2024 = [
    89.165,
    87.472,
    75.915,
    88.197,
    93.660,
    87.241,
    74.746,
    70.270,
    71.742,
    71.383,
    64.314,
    85.819,
    75.227,
    113.159
]

extrapolated_pole_times_2024 = [
    89.165,
    87.472,
    75.915,
    88.197,
    93.660,
    87.241,
    74.746,
    70.270,
    71.742,
    71.383,
    64.314,
    85.819,
    75.227,
    106.168,
    70.030,
    79.757,
    90.447,
    88.340,
    83.241,
    94.186,
    76.629,
    69.484,
    92.189,
    82.908
]

track_list = [
    "Bahrain",
    "Jeddah",
    "Australia",
    "Suzuka",
    "China",
    "Miami",
    "Imola",
    "Monaco",
    "Canada",
    "Spain",
    "Austria",
    "Silverstone",
    "Hungary",
    "Spa",
    "Zandvoort",
    "Monza",
    "Baku",
    "Singapore",
    "Austin",
    "Mexico",
    "Brazil",
    "Las Vegas",
    "Qatar",
    "Abu Dhabi"
]

# from statsf1.com
average_grid_positions = { # indexed based on order in the 2024 calendar (Bahrain, Jeddah, ... Abu Dhabi)
    "VER": [5.64, 5.75, 4.13, 4.38, 8.17, 4.33, 2.0, 7.78, 5.63, 3.4, 2.92, 4.0, 5.1, 7.2, 1.0, 8.78, 4.43, 5.57, 7.25, 3.25, 3.63, 2.0, 4.0, 3.89],
    "PER": [9.21, 2.5, 12.5, 8.5, 10.0, 3.0, 6.75, 11.17, 12.27, 10.0, 10.54, 12.31, 11.57, 6.38, 10.67, 10.15, 5.29, 12.09, 9.91, 8.38, 11.25, 11.0, 15.5, 9.15],
    "HAM": [3.94, 7.75, 4.06, 4.14, 5.5, 9.0, 6.25, 5.47, 2.47, 4.33, 4.23, 4.05, 3.5, 4.0, 6.33, 4.65, 4.14, 2.93, 2.45, 2.88, 5.19, 10.0, 2.0, 2.67],
    "RUS": [9.71, 7.5, 8.5, 10.75, 12.5, 8.33, 10.5, 10.6, 7.75, 12.0, 10.5, 11.5, 13.33, 8.33, 6.67, 10.6, 11.75, 13.33, 11.75, 11.25, 11.0, 3.0, 8.5, 12.2],
    "LEC": [5.75, 5.0, 7.0, 5.2, 9.67, 3.33, 4.0, 6.33, 11.2, 8.14, 7.56, 5.75, 6.86, 7.43, 5.33, 6.33, 4.8, 4.5, 6.0, 5.2, 6.8, 1.0, 9.0, 5.83],
    "SAI": [8.64, 7.33, 8.13, 9.5, 10.5, 2.67, 7.25, 6.89, 11.25, 7.0, 9.0, 9.0, 8.1, 10.1, 5.0, 9.89, 9.14, 7.71, 8.13, 7.13, 10.63, 12.0, 8.5, 10.33],
    "NOR": [10.71, 10.75, 7.0, 6.0, 9.5, 5.0, 5.75, 7.2, 8.0, 7.0, 4.75, 5.57, 4.83, 10.67, 7.33, 7.4, 8.5, 6.33, 5.75, 12.75, 6.75, 15.0, 7.0, 5.0],
    "PIA": [13.0, 6.5, 10.5, 4.0, 5.0, 12.5, 5.0, 6.5, 6.0, 9.0, 10.0, 4.0, 3.0, 5.0, 8.0, 7.0, 10.0, 17.0, 10.0, 7.0, 10.0, 18.0, 6.0, 3.0],
    "ALO": [8.0, 6.5, 8.42, 10.33, 6.31, 9.33, 10.38, 8.1, 6.37, 7.29, 14.08, 9.05, 7.29, 9.63, 9.0, 9.35, 11.33, 7.31, 11.3, 13.29, 8.8, 9.0, 3.5, 9.69],
    "STR": [13.56, 11.5, 13.83, 15.33, 13.75, 13.0, 13.25, 15.57, 15.33, 13.0, 11.9, 13.11, 13.25, 13.63, 11.0, 10.0, 13.0, 17.0, 13.67, 17.33, 14.0, 19.0, 14.0, 13.57],
    "RIC": [8.69, 13.0, 10.0, 11.36, 7.22, 17.0, 6.5, 7.73, 7.4, 9.5, 9.75, 10.21, 10.71, 10.29, 13.5, 10.92, 8.5, 9.9, 8.27, 7.63, 12.75, 14.0, 14.0, 10.62],
    "TSU": [13.5, 13.0, 11.0, 10.67, 19.0, 12.0, 13.0, 11.0, 15.67, 15.25, 12.8, 14.5, 14.75, 16.75, 13.33, 15.33, 7.67, 12.5, 13.33, 16.0, 17.0, 20.0, 9.5, 8.33],
    "HUL": [11.25, 14.0, 10.91, 12.55, 11.0, 10.5, 10.0, 11.64, 9.73, 13.45, 8.75, 9.31, 10.73, 12.73, 14.0, 11.9, 14.8, 10.5, 10.0, 8.83, 8.6, 13.0, 14.0, 9.0],
    "MAG": [13.4, 12.0, 12.0, 14.63, 13.5, 12.67, 14.33, 13.63, 14.38, 12.44, 12.5, 14.4, 15.67, 12.56, 19.0, 13.38, 15.5, 12.0, 13.71, 16.0, 11.0, 8.0, 18.0, 15.13],
    "GAS": [11.25, 10.5, 14.8, 13.17, 12.67, 8.0, 10.25, 9.67, 13.8, 10.14, 9.67, 11.0, 11.71, 10.43, 9.0, 13.0, 12.8, 11.25, 11.0, 13.33, 11.0, 4.0, 4.5, 13.29],
    "OCO": [11.88, 9.25, 12.2, 11.67, 14.0, 13.67, 12.25, 9.33, 9.6, 9.86, 11.22, 11.88, 12.29, 10.25, 12.0, 12.71, 11.6, 13.8, 12.17, 13.5, 14.67, 16.0, 8.5, 11.0],
    "ALB": [11.67, 15.0, 13.25, 12.25, 17.0, 14.33, 12.67, 12.0, 11.0, 14.6, 11.5, 10.5, 14.2, 10.6, 9.5, 7.67, 13.33, 12.67, 9.67, 12.0, 12.33, 5.0, 13.0, 10.75],
    "SAR": [17.6, 19.5, 18.0, 19.5, 20.0, 18.5, 19.0, 15.5, 15.5, 19.5, 18.5, 13.0, 17.0, 18.0, 10.0, 15.0, 14.0, 18.0, 16.0, 19.0, 19.0, 6.0, 15.0, 20.0],
    "BOT": [5.92, 10.0, 12.33, 8.2, 6.25, 10.33, 8.0, 10.0, 7.3, 6.42, 6.69, 8.31, 6.08, 9.67, 12.33, 8.45, 7.43, 9.67, 7.2, 5.63, 7.6, 7.0, 7.5, 9.27],
    "ZHO": [15.0, 14.33, 16.67, 17.67, 16.0, 16.67, 18.5, 19.0, 16.67, 14.33, 16.67, 13.33, 11.67, 18.0, 14.5, 12.5, 14.5, 16.5, 15.0, 11.0, 16.5, 17.0, 19.0, 17.0]
}

# STRATEGY FOR PREDICTING TIMES:
# take each driver's proximity to pole (avg) and use in conjunction with previous year pole time for prediction <- old strategy doesn't account for additional data
# also factoring in average speed increase between pole times of different years
# grid order is self-explanatory once times are obtained

# I think this needs to be done as a dataframe to pass into the model as one object
# Figure out how to format this and if more data is required.

results = []
times = [{}] # list of dictionaries ex. {LEC: 01:10.270}, {VER, 01:18.197}

lap_data = { # will be accessed something like (lap_data['driver'][i] = whatever bullshit)
    'driver': [],
    'track': [],
    'year': [],
    'avg_grid_pos_track': [],
    'track_avg_lap_time': [],
    'temperature': [], # higher temp == slower laps (significant, from tire deg and lower engine RPM)
    'target_time': [] # just get the actual times basically
}

# Converts the default string output from the database into a float that can be worked with
def convert_time(time: str) -> float:
    arr = time.split(':')
    num = 60.00
    num += float(arr[1])
    return num




def get_avg_grid_pos(driver: str) -> float: # should not be needed anymore (dictionary is sufficient)
    match driver:
        case 'VER':
            return # the correct dirver for this position <V>^^^^^


# Retreives the data from the API and writes it to a DataFrame.
def get_data():
    for j in range(22): # Loop through

        session = fastf1.get_session(2023, j+1, "Q") # starting with 2023
        session.load()

        # list of drivers
        drivers = pd.unique(session.laps['Driver']) # list of drivers in format (VER, NOR, HAM)

        for k in range(len(drivers)):
            try:
                ### old code ###
                times[j][drivers[k]] = convert_time(re.findall(r'\d{2}\:\d{2}\.\d{3}', str(session.laps.pick_driver(drivers[k]).pick_fastest()['LapTime']))[0])

                # new code (using more data and different data structure)
                lap_data['driver'].append(drivers[k]) # get driver
                lap_data['track'].append(session.event['Country']) # get track name - figure out how
                lap_data['year'].append(re.findall(r'\d{4}', str(session.date))[0]) # can make this dynamic instead of hardcoding
                lap_data['avg_grid_pos_track'].append(average_grid_positions[drivers[k]]) # in progress, finish the avg_grid list
                lap_data["track_avg_lap_time"].append() # find the average lap time for the track (can do avg for one session or try and do historical avg - hist would be less accurate to current cars)
                lap_data['temperature'].append(session.weather_data['TrackTemp']) # see how this outputs (if it's even correct)
                lap_data["target_time"].append() # what we're predicting (eq. to y in pytorch examples, will compare predicted time to this for model testing)
            except:
                if re.findall(r'\d{2}\:\d{2}', str(session.laps.pick_driver(drivers[k]).pick_fastest()['LapTime'])):
                    times[j][drivers[k]] = convert_time(re.findall(r'(01:\d{2})', str(session.laps.pick_driver(drivers[k]).pick_fastest()['LapTime']))[0] + '.000')

        times.append({})
    times.pop()
    
    # Turn into DataFrame
    df = pd.DataFrame.from_records(times)

    print(df, "\n\n")

    df.mean().sort_values()
    print(df.reindex(df.mean().sort_values().index, axis=1))

    df.to_csv('times.csv')

# Reads the time data from a csv and turns it into a DataFrame
def read_data() -> pd.DataFrame:
    df = pd.read_csv('times.csv')
    return df


# read the data
# data = torch.tensor(read_data().values)

# # Split data into training and testing sets
# train_split = int(0.8 * len(data))
# train_data, test_data = data[:train_split], data[train_split:]

# print(len(train_data), len(test_data))

# # Set manual seed
# torch.manual_seed(42)

# # Instantiate the model
# model = CustomModel()

# # Make predictions
# with torch.inference_mode():
#     preds = model(test_data)

#     print(torch.argmax(torch.softmax(preds, dim=1), dim=1))

# Idea for equalizing data to calculate something
# use Q1 times for everyone but add the average improvement from 10 in Q3 to everyone for track evolution
# downside is that top drivers are not pushing in Q1 so may be inaccurate

# Can alternatively use fastest times for everyone, 
# and then add average improvement from track evolution for Q1 and Q2