import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load the dataset. I use here only July 2023
data = pd.read_csv("data/Bike share ridership 2023-07.csv", encoding='latin1')

pd.set_option('display.max_columns', None)
data.head()

# Extract relevant features
usage_data = data[['Start Station Id', 'End Station Id', 'Trip  Duration']]

# Aggregate the data by start and end stations to calculate usage statistics
start_station_usage = usage_data.groupby('Start Station Id').size().reset_index(name='Start Count')
end_station_usage = usage_data.groupby('End Station Id').size().reset_index(name='End Count')

# Merge the usage statistics
station_usage = pd.merge(start_station_usage, end_station_usage, left_on='Start Station Id', right_on='End Station Id', how='outer').fillna(0)
station_usage.head()
pd.set_option('display.max_rows', None)
station_usage

# Prepare data for clustering
station_usage.fillna(0, inplace=True)
features = station_usage[['Start Count', 'End Count']]

# Standardize the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Determine the optimal number of clusters using the Elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(features_scaled)
    wcss.append(kmeans.inertia_)

# Plot the Elbow graph
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11, 1), wcss, marker='o')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS (Within-Cluster Sum of Square)')
plt.grid(True)
plt.show()

# Apply K-means clustering with 4 clusters (Look at the graph. The elbow is at 3 to 4 clusters)
kmeans = KMeans(n_clusters=4, random_state=42)
station_usage['Cluster'] = kmeans.fit_predict(features_scaled)

# Add cluster labels to the station usage data
station_usage['Cluster'] = kmeans.labels_
station_usage.head()

# Calculate the average start and end counts for each cluster
cluster_summary = station_usage.groupby('Cluster').agg({
    'Start Count': 'mean',
    'End Count': 'mean'
}).reset_index()

# Add a column to show the difference between start and end counts
cluster_summary['Difference'] = cluster_summary['Start Count'] - cluster_summary['End Count']

cluster_summary


# Calculate the difference between start and end counts
station_usage['Difference'] = station_usage['End Count'] - station_usage['Start Count']

# Prepare data for clustering using the difference
features_diff = station_usage[['Difference']]

# Standardize the features
features_scaled_diff = scaler.fit_transform(features_diff)

# Determine the optimal number of clusters using the Elbow method
wcss_diff = []
for i in range(1, 11):
    kmeans_diff = KMeans(n_clusters=i, random_state=45)
    kmeans_diff.fit(features_scaled_diff)
    wcss_diff.append(kmeans_diff.inertia_)

# Plot the Elbow graph for the difference
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss_diff, marker='o')
plt.title('Elbow Method for Optimal Number of Clusters (Difference)')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS (Within-Cluster Sum of Squares)')
plt.grid(True)
plt.show()

# Save the plot as TikZ code
plt.savefig("elbow_chart.tikz", format="pgf")


# Apply K-means clustering with the chosen number of clusters (e.g., 4) based on the difference
kmeans_diff = KMeans(n_clusters=4, random_state=42)
station_usage['Cluster (Difference)'] = kmeans_diff.fit_predict(features_scaled_diff)

# Add cluster labels to the station usage data
station_usage['Cluster (Difference)'] = kmeans_diff.labels_
station_usage.head()

print(station_usage[station_usage['Cluster (Difference)'] == 2])

# Calculate the average difference for each cluster
cluster_summary_diff = station_usage.groupby('Cluster (Difference)').agg({
    'Difference': 'mean'
}).reset_index()

cluster_summary_diff = station_usage.groupby('Cluster (Difference)').agg({
    'Difference': 'mean'
}).reset_index()

mean_difference = station_usage.groupby('Cluster (Difference)')['Difference'].mean()
max_difference = station_usage.groupby('Cluster (Difference)')['Difference'].max()
min_difference = station_usage.groupby('Cluster (Difference)')['Difference'].min()

# Print the results
print(f"Mean Difference: {mean_difference}")
print(f"Maximum Difference: {max_difference}")
print(f"Minimum Difference: {min_difference}")

# Display the cluster summary based on the difference
print(cluster_summary_diff)

# Count the number of stations within each cluster
station_counts = station_usage.groupby('Cluster (Difference)').size().reset_index(name='Station Count')

# Display the station counts
station_counts

# Extract location data
location_data = data[['Start Station Id', 'Start Station Name']]
location_data = location_data.drop_duplicates()

station_usage_location = pd.merge(station_usage, location_data, on='Start Station Id')
station_usage_location['station_id'] = station_usage_location['Start Station Id'].astype(int)
station_usage_location.head()

station_usage_location.to_csv('station_usage_location.csv', index=False) 




# getting station location
import geopandas as gpd
gdf = gpd.read_file('toronto_bike_share_stations.geojson')
# Convert GeoDataFrame to pandas DataFrame
station_locations = pd.DataFrame(gdf.drop(columns='geometry'))

# Display the first few rows of the DataFrame
print(station_locations.head())

# Merge to get lat lon
station_usage_location = pd.merge(station_usage_location, station_locations[['station_id', 'lat', 'lon']], on='station_id', how='left')

# Display the merged DataFrame
station_usage_location.head()


import folium
from geopy.geocoders import Nominatim

# Load your data from the CSV file (replace with your actual file path)
# file_path = "station_usage_location.csv"
df = station_usage_location.dropna(subset=['lat'])
df_with_na_lat = station_usage_location[station_usage_location['lat'].isna()]
print(df_with_na_lat)

# Initialize geocoder - to find lat lon if we don't have
# geolocator = Nominatim(user_agent="bike_station_geocoder")

# Geocode addresses to get latitude and longitude
# for index, row in df.iterrows():
#     location = geolocator.geocode(row["Start Station Name"] + ", Toronto, ON")
#     if location:
#         df.at[index, "Latitude"] = location.latitude
#         df.at[index, "Longitude"] = location.longitude
#     else:
#         print(f"Geocoding failed for station: {row['Start Station Name']}")

# Create a map centered around Toronto
toronto_map = folium.Map(location=[43.70, -79.40], zoom_start=13)

cluster_colors = {
    0: 'green',
    1: 'blue',
    2: 'purple',
    3: 'red'
}


# Add markers for each station
for index, row in df.iterrows():
    cluster = row['Cluster (Difference)']
    color = cluster_colors.get(cluster, 'gray')  # Default to gray if cluster is not found
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"Station: {row['station_id']}, Cluster: {cluster}",
        icon=folium.Icon(color=color),
    ).add_to(toronto_map)

# Save the map as an HTML file
toronto_map.save("toronto_bike_stations_map.html")


