# Toronto Bike Share Analysis

## Overview

This project analyzes Toronto's Bike Share ridership data for July 2023. The analysis involves clustering bike stations based on their usage patterns, calculating differences between start and end counts, and visualizing the results using interactive maps. The goal is to understand bike usage patterns and identify stations that are over- or under-utilized, providing insights for potential improvements in bike distribution and station management.

## Data Sources

- **Bike Share Ridership Data**: Downloaded from [Toronto Open Data Portal](https://open.toronto.ca/).
- **Bike Share Station Locations**: Downloaded from [ArcGIS REST Services](https://services.arcgis.com/As5CFN3ThbQpy8Ph/arcgis/rest/services/Toronto_Bike_Share_Locations/FeatureServer/0/query).

## Analysis Steps

### Data Loading and Preprocessing

- The project begins by loading the July 2023 ridership data and the station locations.
- Relevant features such as 'Start Station Id', 'End Station Id', and 'Trip Duration' are extracted, and usage statistics are calculated for each station.
- The data is aggregated by start and end stations to get the total counts for each station, which are then merged to create a comprehensive usage dataset.

### Clustering Analysis

- **Standardization**: The data is standardized to ensure that all features contribute equally to the clustering process.
- **Elbow Method**: The optimal number of clusters is determined using the Elbow method, which involves plotting the within-cluster sum of squares (WCSS) against the number of clusters to identify the point where adding more clusters yields diminishing returns.
- **K-means Clustering**: K-means clustering is applied based on the start and end counts, as well as the difference between them. This identifies stations that are similarly utilized and those that have significant differences between bike pickups and drop-offs.

### Visualization

- An interactive map centered around Toronto is created using `folium`.
- Bike stations are marked on the map, with colors representing their cluster categories. This provides a visual representation of station utilization patterns.
- The map helps to easily identify areas with high discrepancies in bike usage, aiding in the planning and optimization of bike distribution.

## Results

### Clustering Summary

- The clustering analysis revealed distinct patterns in bike station usage. Stations were grouped into four clusters based on their start and end counts.
- **Cluster 0**: Represents stations with balanced usage.
- **Cluster 1**: Indicates stations with slightly higher start counts than end counts.
- **Cluster 2**: Identifies stations with higher end counts than start counts, suggesting these are popular drop-off points.
- **Cluster 3**: Highlights stations with significant discrepancies between start and end counts.

### Key Findings

- **Balanced Stations**: A majority of stations fell into Cluster 0, indicating balanced usage.
- **Over-Utilized Stations**: Stations in Cluster 2 were identified as over-utilized drop-off points, which may require additional bikes to meet demand.
- **Under-Utilized Stations**: Stations in Cluster 3 had significant discrepancies, indicating potential inefficiencies in bike distribution.

### Interactive Map

- The interactive map (`toronto_bike_stations_map.html`) visually presents the clustering results, with each station color-coded by its cluster category.
- Pop-up information on the map provides details on each station's ID and cluster category, making it easy to explore and understand the usage patterns.

## Conclusion

The Toronto Bike Share Analysis project provides valuable insights into bike usage patterns and station utilization. By identifying over- and under-utilized stations, the analysis supports informed decision-making for optimizing bike distribution and improving the overall efficiency of the bike share system.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.