import fastf1
import pandas as pd

from fastf1.core import Laps

pole_laps = []

# for i in range(14):
#     session = fastf1.get_session(2024, i+1, 'Q')
#     session.load()

#     drivers = pd.unique(session.laps['Driver'])

#     list_fastest_laps = list()
#     for drv in drivers:
#         drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
#         list_fastest_laps.append(drvs_fastest_lap)
#     fastest_laps = Laps(list_fastest_laps) \
#     .sort_values(by='LapTime') \
#     .reset_index(drop=True)
    
#     pole_lap = fastest_laps.pick_fastest()
#     pole_laps.append(pole_lap['LapTime'])

# for lap in pole_laps:
#     print(lap)

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
    106.168
]

# avg_difference = 0

# for i in range(14):
#     avg_difference += pole_times_2023[i] - pole_times_2024[i]
# avg_difference /= 14

# print(avg_difference)

session = fastf1.get_session(2024, '1', "Q")
session.load()

# list of drivers
drivers = pd.unique(session.laps['Driver'])

print(drivers)

print(session.laps.pick_driver(1).pick_fastest())