import pandas as pd
from math import atan2, degrees, radians, cos

def calculate_2d_bearing(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate differences
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1

    # Adjust differences for latitude scale
    x = d_lon * cos((lat1 + lat2) / 2)
    y = d_lat

    # Calculate the angle in radians and convert to degrees
    angle = atan2(x, y)
    bearing = (degrees(angle) + 360) % 360

    return bearing

def get_2d_direction(bearing):
    # Convert bearing angle to a 2D cardinal direction, including intercardinal directions.
    if bearing >= 337.5 or bearing < 22.5:
        return 'N'
    elif 22.5 <= bearing < 67.5:
        return 'NE'
    elif 67.5 <= bearing < 112.5:
        return 'E'
    elif 112.5 <= bearing < 157.5:
        return 'SE'
    elif 157.5 <= bearing < 202.5:
        return 'S'
    elif 202.5 <= bearing < 247.5:
        return 'SW'
    elif 247.5 <= bearing < 292.5:
        return 'W'
    else:  # 292.5 <= bearing < 337.5
        return 'NW'

def get_adjacent_directions(direction):
    # Define a mapping of each direction to its adjacent directions
    adjacent = {
        'N': ['NW', 'NE'],
        'NE': ['N', 'E'],
        'E': ['NE', 'SE'],
        'SE': ['E', 'S'],
        'S': ['SE', 'SW'],
        'SW': ['S', 'W'],
        'W': ['SW', 'NW'],
        'NW': ['W', 'N']
    }
    return adjacent[direction]

# Load the airports data
airports_df = pd.read_csv('airports_large.csv')

# Define the origin and destination airport IATA codes
origin_iata = "LGW"
destination_iata = "DPS"

# Find the origin and destination airports' coordinates
# origin_airport = airports_df.loc[airports_df['iata_code'] == origin_iata].iloc[0]
# destination_airport = airports_df.loc[airports_df['iata_code'] == destination_iata].iloc[0]

# Find the origin and destination airports' ident
origin_airport = airports_df.loc[airports_df['iata_code'] == origin_iata, 'ident'].iloc[0]
destination_airport = airports_df.loc[airports_df['iata_code'] == destination_iata, 'ident'].iloc[0]

# Find the coordinates for origin and destination airports
# origin_coords = (origin_airport['latitude_deg'], origin_airport['longitude_deg'])
# destination_coords = (destination_airport['latitude_deg'], destination_airport['longitude_deg'])

origin_coords = airports_df.loc[airports_df['ident'] == origin_airport, ['latitude_deg', 'longitude_deg']].iloc[0]
destination_coords = airports_df.loc[airports_df['ident'] == destination_airport, ['latitude_deg', 'longitude_deg']].iloc[0]



# Calculate the direction of the destination airport from the origin
# destination_bearing = calculate_2d_bearing(origin_coords[0], origin_coords[1], destination_coords[0], destination_coords[1])

destination_bearing = calculate_2d_bearing(*origin_coords, *destination_coords)

destination_direction = get_2d_direction(destination_bearing)
adjacent_directions = get_adjacent_directions(destination_direction)

# Prepare a list to hold the data for airports in the destination direction and adjacent directions
filtered_csv_data = []

# Iterate over the airports and calculate the direction from the origin
for _, airport in airports_df.iterrows():
    if airport['iata_code'] != origin_iata:  # Exclude the origin airport
        dest_lat = airport['latitude_deg']
        dest_lon = airport['longitude_deg']
        bearing = calculate_2d_bearing(origin_coords[0], origin_coords[1], dest_lat, dest_lon)
        direction = get_2d_direction(bearing)
        
        # Include only airports in the destination direction or adjacent directions
        if direction == destination_direction or direction in adjacent_directions:
            filtered_csv_data.append({
                'airport_name': airport['name'],
                'municipality': airport['municipality'],
                'iata_code': airport['iata_code'],
                'ident':airport['ident'],
                'direction_from_origin': direction
            })

# Convert the list of data to a new DataFrame
filtered_airports_df = pd.DataFrame(filtered_csv_data)

# Define the path for the new CSV file
filtered_csv_file_path = 'airports_directions_from_origin.csv'

# Write the new DataFrame to a CSV file
filtered_airports_df.to_csv(filtered_csv_file_path, index=False)

# Output the file path
print(f"The filtered CSV file is saved at: {filtered_csv_file_path}")
