import pandas as pd

df = pd.read_csv('times.csv')

print(df, '\n\n')

# df.mean().sort_values()
# print(df.reindex(df.mean().sort_values().index, axis=1))

data = {
    'driver': ['VER', 'LEC', 'HAM', 'VER', 'LEC', 'HAM'],
    'track': ['Bahrain', 'Bahrain', 'Bahrain', 'Monaco', 'Monaco', 'Monaco'],
    'avg_lap_time_track': [89.5, 89.8, 90.2, 105.1, 105.6, 106.0],
    'avg_quali_pos_track': [1.5, 2.0, 3.0, 2.0, 1.0, 3.0], 
    'track_avg_lap_time': [92.0, 92.0, 92.0, 108.0, 108.0, 108.0],
    'temperature': [25, 25, 25, 20, 20, 20],
    'target_lap_time': [89.2, 89.6, 90.0, 104.8, 105.2, 105.7]  # Example target variable
}
df = pd.DataFrame(data)
print(df.driver.to_string(index=False))