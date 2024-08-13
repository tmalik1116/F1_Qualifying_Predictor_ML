import fastf1
import pandas as pd
import re
import torch

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

# STRATEGY FOR PREDICTING TIMES:
# take each driver's proximity to pole (avg) and use in conjunction with previous year pole time for prediction
# also factoring in average speed increase between pole times of different years
# grid order is self-explanatory once times are obtained

# I think this needs to be done as a dataframe to pass into the model as one object
# Figure out how to format this and if more data is required.


def convert_time(time: str) -> float:
    arr = time.split(':')
    num = 60.00
    num += float(arr[1])
    return num

results = []
times = [{}] # list of dictionaries ex. {LEC: 01:10.270}, {VER, 01:18.197}


for i in range(14):
    session = fastf1.get_session(2024, i+1, "Q")
    session.load()
    results.append(str(session.results.loc[:, ['Abbreviation', 'Q3']]).split('\n'))
    # results[]
for j in range(len(results)): # Loop through
    # print(f" LENGTH:    {len(results[j])}")
    for k in range(1, len(results[j])):
        # print(k)
        item = str(results[j][k]).split()
        # print(item)
        # print(j)

        try:
            times[j][re.findall(r'[A-Z]{3}', item[1])[0]] = convert_time(re.findall(r'\d{2}\:\d{2}\.\d{3}', item[4])[0])
        except:
            times[j][re.findall(r'[A-Z]{3}', item[1])[0]] = 150.000

    times.append({})
times.pop()
    #     times[i-1].update({re.findall(r'[A-Z]{3}', str(results[i-1][j])): float(re.findall(r'\d{2}\:\d{2}\.\d{3}', str(results[i-1][j])))})

    
    # print(session.results)

    # print(session.results.loc[:, ['Abbreviation', 'Q3']])



# for result in results:
#     print(result) # something like this but maybe Q1
    # then parse the time only from this output format
    # and can either also grab driver abbreviation from API or implement my own function based on number



for time in times:
    print(f"{dict(sorted(time.items(), key=lambda item: item[1]))}\n\n")

print(len(times))

# Idea for equalizing data to calculate something
# use Q1 times for everyone but add the average improvement from 10 in Q3 to everyone for track evolution
# downside is that top drivers are not pushing in Q1 so may be inaccurate

# Can alternatively use fastest times for everyone, 
# and then add average improvement from track evolution for Q1 and Q2