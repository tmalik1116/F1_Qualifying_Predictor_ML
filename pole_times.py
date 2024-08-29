import fastf1
import pandas as pd
import re
# import FastF1_testing

from fastf1.core import Laps
from fastf1.ergast import Ergast


num_races = [19, 19, 21, 20]

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

# df = session._drivers_results_from_ergast(load_drivers=True, load_results=True)
# df = df.drop(labels=['DriverNumber', 'TeamId', 'DriverId', 'LastName', 'FirstName', 'FullName'], axis=1)
# print(df)

# # for index, row in df.iterrows():
# #     print(row['Abbreviation'], row['Q3'])

erg = Ergast('pandas')

# don't understand this object, read https://docs.fastf1.dev/ergast.html#fastf1.ergast.interface.ErgastMultiResponse
result = erg.get_qualifying_results(
                                     season=2017,
                                        round=3,
                                        result_type='pandas'
                                        )

print(result.content[0]['Q3'].iloc[3])

new_dict = result.content[0].to_dict()

print(new_dict.keys())

for key in new_dict: # invert all internal dictionaries
    new_dict[key] = {v: k for k, v in new_dict[key].items()}

print(new_dict.keys())

print(new_dict['Q3'])

drivers = new_dict['driverCode'].keys()

for driver in drivers:
    print(driver)
    

# print(result.content[0])

year = 2014
for num in num_races:
    for j in range(num):

        session = fastf1.get_session(year, 
                             j+1, 
                             "Q",
                             'ergast')
        session.load()

        track = re.findall()

        for i in range(20): # use this to create more dataset entries (how far back?)
            if i < 10:
                try:
                    print(re.findall(r'[A-Z]{3}', str(df.iloc[i]))[0], re.findall(r'0\d\:\d{2}\.\d{3}', str(df.iloc[i]))[2]) # get driver, Q3 time (HAM 01:23.456)
                except:
                    continue # skip entry if no lap time set, not relevant
            elif i < 15:
                try:
                    print(re.findall(r'[A-Z]{3}', str(df.iloc[i]))[0], re.findall(r'0\d\:\d{2}\.\d{3}', str(df.iloc[i]))[1]) # get driver, Q2 time (HAM 01:23.456)
                except:
                    continue # skip entry if no lap time set, not relevant
            else:
                try:
                    print(re.findall(r'[A-Z]{3}', str(df.iloc[i]))[0], re.findall(r'0\d\:\d{2}\.\d{3}', str(df.iloc[i]))[0]) # get driver,  Q1 time (HAM 01:23.456)
                except:
                    continue # skip entry if no lap time set, not relevant


print(re.findall(r'\S\S+', str(result.description['country']))[0]) # can retreive country and locality and use whatever matches 