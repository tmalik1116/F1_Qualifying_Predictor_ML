import fastf1
import pandas as pd
from datetime import datetime
import numpy as np
import os

# 1. Set up Caching
# It's highly recommended to enable caching to speed up data loading and reduce API calls.
# Create a 'cache' directory in your script's location or specify a path.
cache_dir = os.path.join(os.getcwd(), 'fastf1_cache')
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
fastf1.Cache.enable_cache(cache_dir)
print(f"FastF1 cache enabled at: {cache_dir}")

def get_average_grid_positions():
    current_year = datetime.now().year
    print(f"Analyzing F1 data up to the current year: {current_year}")

    # 2. Get Current Season Information to identify current drivers and tracks
    try:
        current_schedule = fastf1.get_event_schedule(current_year)
        print(f"Fetched schedule for {current_year} season.")
    except Exception as e:
        print(f"Error fetching current season schedule: {e}. Please ensure the season data is available.")
        print("FastF1 timing data, telemetry, and position data are available from 2018 onwards. Schedule information and session results are available for older seasons too (limited to Ergast web API).")
        return pd.DataFrame()

    # 3. Collect Current Drivers and Tracks
    current_drivers_ids = set()
    # Use a dictionary to map FastF1's internal CircuitId to a readable track name
    current_tracks_map = {} # {circuitId: "Location - OfficialEventName"}
    current_track_names_from_schedule = set() # To quickly check if a track from a past season is a 'current' track

    # Get all circuits from the current schedule using 'Location' and 'OfficialEventName'
    for _, event in current_schedule.iterrows():
        # Only consider conventional race weekends for track identification
        if event['EventFormat'] == 'conventional':
            track_name = f"{event['Location']} - {event['OfficialEventName'].split(' Grand Prix')[0]}"
            current_track_names_from_schedule.add(track_name)
    print(f"Identified {len(current_track_names_from_schedule)} current tracks based on schedule.")

    # To get current drivers, we need to load results from at least one race in the current season.
    current_season_races = current_schedule[current_schedule['EventFormat'] == 'conventional']
    if not current_season_races.empty:
        latest_race_event = None
        for i in range(len(current_season_races) - 1, -1, -1):
            event = current_season_races.iloc[i]
            try:
                session = fastf1.get_session(current_year, event['RoundNumber'], 'R')
                session.load(telemetry=False, laps=False, weather=False)
                if not session.results.empty:
                    latest_race_event = event
                    # Populate current_tracks_map with actual CircuitId from a loaded session
                    if 'CircuitId' in session.event and pd.notna(session.event['CircuitId']):
                        track_name = f"{session.event['Location']} - {session.event['OfficialEventName'].split(' Grand Prix')[0]}"
                        current_tracks_map[session.event['CircuitId']] = track_name
                    break
            except Exception:
                continue

        if latest_race_event is not None:
            print(f"Loading results from {latest_race_event['OfficialEventName']} ({current_year}) to identify current drivers.")
            session = fastf1.get_session(current_year, latest_race_event['RoundNumber'], 'R')
            session.load(telemetry=False, laps=False, weather=False)
            current_drivers_ids.update(session.results['DriverId'].unique())
            print(f"Identified {len(current_drivers_ids)} current drivers.")
        else:
            print("Could not load any race results for the current season to identify drivers. This might happen early in the season.")
    else:
        print("No conventional races found in the current season schedule.")

    if not current_drivers_ids:
        print("No current drivers identified. Exiting.")
        return pd.DataFrame()

    all_driver_grid_positions = {}

    # 4. Gather Career Grid Positions
    start_career_year = 2000
    if current_year < start_career_year:
        start_career_year = current_year

    for driver_id in current_drivers_ids:
        driver_name = ""
        # Initialize with CircuitIds found in current_tracks_map
        driver_positions_on_tracks = {circuit_id: [] for circuit_id in current_tracks_map.keys()}

        print(f"\nProcessing driver: {driver_id}...")
        for year in range(start_career_year, current_year + 1):
            try:
                season_schedule = fastf1.get_event_schedule(year)
            except Exception:
                continue

            for _, event in season_schedule.iterrows():
                if event['EventFormat'] != 'conventional':
                    continue

                # Check if the track name from this historical event matches any current track
                event_track_name = f"{event['Location']} - {event['OfficialEventName'].split(' Grand Prix')[0]}"
                if event_track_name not in current_track_names_from_schedule:
                    continue

                try:
                    session = fastf1.get_session(year, event['RoundNumber'], 'R')
                    session.load(telemetry=False, laps=False, weather=False)

                    if not session.results.empty and 'CircuitId' in session.event and pd.notna(session.event['CircuitId']):
                        circuit_id = session.event['CircuitId']
                        # Ensure this circuit_id is one of the 'current' tracks we care about
                        if circuit_id in current_tracks_map:
                            driver_results = session.results[session.results['DriverId'] == driver_id]
                            if not driver_results.empty:
                                grid_position = driver_results.iloc[0]['GridPosition']
                                if pd.notna(grid_position) and grid_position > 0:
                                    driver_positions_on_tracks[circuit_id].append(int(grid_position))
                                    if not driver_name:
                                        driver_name = f"{driver_results.iloc[0]['GivenName']} {driver_results.iloc[0]['FamilyName']}"
                    elif not session.results.empty:
                         # Fallback for older data where CircuitId might be missing in session.event
                        print(f"Warning: 'CircuitId' not found in session.event for {event['OfficialEventName']} ({year}). Skipping for driver {driver_id}.")
                except Exception as e:
                    pass

        all_driver_grid_positions[driver_id] = {
            'DriverName': driver_name if driver_name else driver_id,
            'Tracks': driver_positions_on_tracks
        }

    # 5. Calculate Averages
    final_results = []
    for driver_id, data in all_driver_grid_positions.items():
        driver_name = data['DriverName']
        for circuit_id, positions in data['Tracks'].items():
            if positions:
                avg_grid_pos = np.mean(positions)
                final_results.append({
                    'Driver': driver_name,
                    'Track': current_tracks_map[circuit_id],
                    'AverageGridPosition': round(avg_grid_pos, 2),
                    'RacesCount': len(positions)
                })

    # 6. Present Results
    df_results = pd.DataFrame(final_results)
    if not df_results.empty:
        df_results = df_results.sort_values(by=['Driver', 'Track']).reset_index(drop=True)

    return df_results

if __name__ == "__main__":
    avg_grid_df = get_average_grid_positions()
    if not avg_grid_df.empty:
        print("\nAverage Grid Positions for Current F1 Drivers on Current Tracks (Career):")
        print(avg_grid_df.to_string())
    else:
        print("No data to display or an error occurred.")