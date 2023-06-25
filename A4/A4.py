"""
This script retrieves the latest earthquake data from the USGS Website
and interactively displays it on a map

Data source : https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php

Author: Mohamed Dhia TURKI
"""
import pandas as pd
import geopandas as gpd
#from shapely.geometry import Point
import folium


#add function to create a custom map

def load_earthquake_data(csv_path):
    """
    Load earthquake data from a CSV file location.

    Args:
        csv_path (str) -- link to daily, weekly, monthly earhquakes.

    Returns:
        data -- The loaded earthquake data.
    """
    data = pd.read_csv(csv_path)
    return data

def convert_to_geodataframe(data, longitude, latitude):
    """
    Convert the  retrieved DataFrame to a GeoDataFrame with Point geometries.

    Args:
    data (pandas.DataFrame) -- The DataFrame containing earthquake data.
        longitude (str) -- The column name for longitude values.
        latitude(str) -- The column name for latitude values.

    Returns:
        gdf -- The converted GeoDataFrame.
    """
    gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data[longitude], data[latitude]))

    return gdf


def filter_earthquakes_by_magnitude(gdf, min_mag, max_mag=None):
    """
    Filter earthquake data based on a specific mag range.

    Args:
        gdf (geopandas.GeoDataFrame) --  GeoDataFrame containing earthquake data.
        min_mag (float) --  minimum mag to include.
        max_mag (float, optional) --  maximum mag to include. Defaults to None.

    Returns:
        filtered -- The filtered GeoDataFrame.
    """
    if max_mag:
        filtered = gdf[(gdf['mag'] >= min_mag) & (gdf['mag'] <= max_mag)]
    else:
        filtered = gdf[gdf['mag'] >= min_mag]
    return filtered

def plot_earthquake_map(filtered):
    """
    Plot an interactive map with earthquake data.

    Args:
        gdf_filtered (geopandas.GeoDataFrame): Filtered GeoDataFrame containing earthquake data.

    Returns:
        folium.Map: The interactive map with earthquake markers and popups.
    """
    # Create a map object
    m = folium.Map()

    # Iterate to get point attributes from gdf
    for idx, row in filtered.iterrows():
        time = row['time']
        magnitude = row['mag']
        place = row['place']
        geometry = row['geometry']

        # Create popup
        popup_content = f"<strong>Time:</strong> {time}<br><strong>Magnitude:</strong> {magnitude}<br><strong>Place:</strong> {place}"

        # Create markers with custom styles according to magnitude
        if magnitude < 4.0:
            color = 'green'
            size = 5
        elif magnitude < 6.0:
            color = 'orange'
            size = 7
        else:
            color = 'red'
            size = 9

        # Extract the latitude and longitude from the geometry
        latitude, longitude = geometry.y, geometry.x

        # Add the marker with popup to the map
        folium.CircleMarker(
            location=[latitude, longitude],
            radius=size,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_content, max_width=250)
        ).add_to(m)

    return m