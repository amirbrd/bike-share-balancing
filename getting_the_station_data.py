import requests
import json

# REST endpoint for Toronto Bike Share Locations
rest_endpoint = "https://services.arcgis.com/As5CFN3ThbQpy8Ph/arcgis/rest/services/Toronto_Bike_Share_Locations/FeatureServer/0/query"
# rest_endpoint = "https://services9.arcgis.com/nRr1Oi5qh5ty5nXz/arcgis/rest/services/Summarize_StationsApril6_within_TorontoNeighbourhoods/FeatureServer/0query"


# Parameters for the query
params = {
    'where': '1=1',  # Select all features
    'outFields': '*',  # Select all fields
    'f': 'geojson'  # Get data in GeoJSON format
}

# Make the request
response = requests.get(rest_endpoint, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Save the data to a file
    with open('toronto_bike_share_stations.geojson', 'w') as file:
        json.dump(data, file)
    
    print("Data downloaded and saved to toronto_bike_share_stations.geojson")
else:
    print(f"Failed to fetch data: {response.status_code}")

# If needed, load and display the data
import geopandas as gpd

gdf = gpd.read_file('toronto_bike_share_stations.geojson')
print(gdf.head())
