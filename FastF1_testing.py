import fastf1
import pandas as pd
import re
import torch


def convert_time(time: str) -> float:
    arr = time.split(':')
    num = 60.00
    num += float(arr[1])
    return num

results = []
times = [{str: float}] # list of dictionaries ex. {LEC: 01:10.270}, {VER, 01:18.197}


for i in range(14):
    session = fastf1.get_session(2024, i+1, "Q")
    session.load()
    results.append(str(session.results.loc[:, ['Abbreviation', 'Q1']]).split('\n'))
    # results[]
for j in range(len(results)): # Loop through
    print(f" LENGTH:    {len(results[j])}")
    for k in range(1, len(results[j])):
        print(k)
        item = str(results[j][k]).split()
        print(item)
        print(j)

        try:
            times[j][re.findall(r'[A-Z]{3}', item[1])[0]] = convert_time(re.findall(r'\d{2}\:\d{2}\.\d{3}', item[4])[0])
        except:
            times[j][re.findall(r'[A-Z]{3}', item[1])[0]] = None

        times.append({})
    #     times[i-1].update({re.findall(r'[A-Z]{3}', str(results[i-1][j])): float(re.findall(r'\d{2}\:\d{2}\.\d{3}', str(results[i-1][j])))})

    
    # print(session.results)

    # print(session.results.loc[:, ['Abbreviation', 'Q3']])



for result in results:
    print(result) # something like this but maybe Q1
    # then parse the time only from this output format
    # and can either also grab driver abbreviation from API or implement my own function based on number



for time in times:
    print(time)

# Idea for equalizing data to calculate something
# use Q1 times for everyone but add the average improvement from 10 in Q3 to everyone for track evolution
# downside is that top drivers are not pushing in Q1 so may be inaccurate

# Can alternatively use fastest times for everyone, 
# and then add average improvement from track evolution for Q1 and Q2