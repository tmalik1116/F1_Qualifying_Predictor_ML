import fastf1
import pandas as pd
import re
import F1_Quali

from fastf1.core import Laps
from fastf1.ergast import Ergast


num_races = [19, 19, 21, 20]

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



# print(f"{session.results['Abbreviation']} {session.results['Q3']}")
# for result in session.results['Q3']:
#     print(result, session._drivers_results_from_ergast())

# print(session.results['Q3'], session.results['Abbreviation'])

# print(df)

# # for index, row in df.iterrows():
# #     print(row['Abbreviation'], row['Q3'])

erg = Ergast('pandas')

# don't understand this object, read https://docs.fastf1.dev/ergast.html#fastf1.ergast.interface.ErgastMultiResponse

# print(result.content[0]['Q3'].iloc[3])

# new_dict = result.content[0].to_dict()

# print(new_dict.keys())

# for key in new_dict: # invert all internal dictionaries
#     new_dict[key] = {v: k for k, v in new_dict[key].items()}
# print(new_dict)

# print(new_dict.keys())

# print(new_dict['Q3'])

# drivers = new_dict['driverCode'].keys()

# print(result.content[0])

year = 2014
for num in num_races:
    for j in range(num):
        result = erg.get_qualifying_results(
                                     season=year,
                                        round=j+1,
                                        result_type='pandas'
                                        )
        data = result.content[0]
        data.to_csv('test.csv')
        locality =  str(result.description['locality']).split()[1]
        country = str(result.description['country']).split()[1]
        print(locality, country)

        if country in track_list.keys():
            track = country
        elif locality.__contains__('Yas Marina'):
            track = 'Abu Dhabi'
        else:
            track = locality
        # df = session._drivers_results_from_ergast(load_drivers=True, load_results=True)
        # df = df.drop(labels=['DriverNumber', 'TeamId', 'DriverId', 'LastName', 'FirstName', 'FullName'], axis=1)

        for i in range(20): # use this to create more dataset entries (how far back?)
            print(str(data.iloc[i]))
            if i < 10: # driver made it to Q3
                
                try: 
                    lap_data['target_time'].append(re.findall(r'0\d\:\d{2}\.\d{3}', str(data.iloc[i]))[2])
                except:
                    continue # skip entry if no lap time set, not relevant
            elif i < 15: # driver made it to Q2
                try:
                    lap_data['target_time'].append(re.findall(r'0\d\:\d{2}\.\d{3}', str(data.iloc[i]))[1])
                except:
                    continue
            else: # driver made it to Q1
                try:
                    lap_data['target_time'].append(re.findall(r'0\d\:\d{2}\.\d{3}', str(data.iloc[i]))[0])
                except:
                    continue

            # Code is same for all cases
            lap_data['driver'].append(re.findall(r'[A-Z]{3}', str(data.iloc[i]))[0])
            lap_data["track"].append(track)


print(lap_data['driver'])
print(len(lap_data["driver"]))


# print(re.findall(r'\S\S+', str(result.description['country']))[0]) # can retreive country and locality and use whatever matches 