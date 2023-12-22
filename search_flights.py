import http.client
import pandas as pd
from datetime import datetime

# Load the filtered airports data
filtered_csv_file_path = 'airports_directions_from_origin.csv'
filtered_airports_df = pd.read_csv(filtered_csv_file_path)

# Setup for Flightera Flight Data API
conn = http.client.HTTPSConnection("flightera-flight-data.p.rapidapi.com")
headers = {
    'X-RapidAPI-Key': "ea889421a4msh88f3a3c53c1fbbcp111642jsn24439c513763",
    'X-RapidAPI-Host': "flightera-flight-data.p.rapidapi.com"
}

# Define the origin airport ident
origin_ident = "EGKK"  # LGW

# Define the date and time for the flight search
search_datetime = "2023-12-23T12:00:00.000Z"

# Iterate over the first 10 airports in the filtered list
for index, airport in filtered_airports_df.head(1).iterrows():
    destination_ident = 'LFPG' # airport['ident']

    # API request for flights from origin to this destination airport
    request_path = f"/airport/flights?direction=departure&ident={origin_ident}&time={search_datetime}&counterpart_ident={destination_ident}"
    conn.request("GET", request_path, headers=headers)

    res = conn.getresponse()
    data = res.read()

    # Print the response data
    print(f"Flights from {origin_ident} to {destination_ident}:")
    print(data.decode("utf-8"))
    print("\n")  # New line for readability between requests
