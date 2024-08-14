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

# from statsf1.com
average_grid_positions = { # indexed based on order in the 2024 calendar (Bahrain, Jeddah, ... Abu Dhabi)
    "VER": [5.64, 5.75, 4.13, 4.38, 8.17, 4.33, 2.0, 7.78, 5.63, 3.4, 2.92, 4.0, 5.1, 7.2, 1.0, 8.78, 4.43, 5.57, 7.25, 3.25, 3.63, 2.0, 4.0, 3.89],
    "PER": [9.21, 2.5, 12.5, 8.5, 10.0, 3.0, 6.75, 11.17, 12.27, 10.0, 10.54, 12.31, 11.57, 6.38, 10.67, 10.15, 5.29, 12.09, 9.91, 8.38, 11.25, 11.0, 15.5, 9.15],
    "HAM": [3.94, 7.75, 4.06, 4.14, 5.5, 9.0, 6.25, 5.47, 2.47, 4.33, 4.23, 4.05, 3.5, 4.0, 6.33, 4.65, 4.14, 2.93, 2.45, 2.88, 5.19, 10.0, 2.0, 2.67],
    "RUS": [9.71, 7.5, 8.5, 10.75, 12.5, 8.33, 10.5, 10.6, 7.75, 12.0, 10.5, 11.5, 13.33, 8.33, 6.67, 10.6, 11.75, 13.33, 11.75, 11.25, 11.0, 3.0, 8.5, 12.2],
    "LEC": [5.75, 5.0, 7.0, 5.2, 9.67, 3.33, 4.0, 6.33, 11.2, 8.14, 7.56, 5.75, 6.86, 7.43, 5.33, 6.33, 4.8, 4.5, 6.0, 5.2, 6.8, 1.0, 9.0, 5.83],
    "SAI": [],
    "NOR": [],
    "PIA": [],
    "ALO": [],
    "STR": [],
    "RIC": [],
    "TSU": [],
    "HUL": [],
    "MAG": [],
    "GAS": [],
    "OCO": [],
    "ALB": [],
    "SAR": [],
    "BOT": [],
    "ZHO": []
}

# STRATEGY FOR PREDICTING TIMES:
# take each driver's proximity to pole (avg) and use in conjunction with previous year pole time for prediction
# also factoring in average speed increase between pole times of different years
# grid order is self-explanatory once times are obtained

# I think this needs to be done as a dataframe to pass into the model as one object
# Figure out how to format this and if more data is required.


# Converts the default string output from the database into a float that can be worked with
def convert_time(time: str) -> float:
    arr = time.split(':')
    num = 60.00
    num += float(arr[1])
    return num


results = []
times = [{}] # list of dictionaries ex. {LEC: 01:10.270}, {VER, 01:18.197}

lap_data = {
    'driver': [],
    'track': [],
    'year': [],
    'avg_grid_pos_track': [],
    'track_avg_lap_time': [],
    'temperature': [],
    'target_time': []
}


def get_avg_grid_pos(driver: str) -> float:
    match driver:
        case 'VER':
            return 


# Retreives the data from the API and writes it to a DataFrame.
def get_data():
    for j in range(22): # Loop through

        session = fastf1.get_session(2023, j+1, "Q")
        session.load()

        # list of drivers
        drivers = pd.unique(session.laps['Driver']) # list of drivers in format (VER, NOR, HAM)

        for k in range(len(drivers)):
            try:
                # old code
                times[j][drivers[k]] = convert_time(re.findall(r'\d{2}\:\d{2}\.\d{3}', str(session.laps.pick_driver(drivers[k]).pick_fastest()['LapTime']))[0])

                # new code (using more data and different data structure)
                lap_data['driver'].append(drivers[k]) # get driver
                lap_data['track'].append(session.event['Country']) # get track name - figure out how
                lap_data['year'].append(2023)
                lap_data['avg_grid_pos_track'].append()
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