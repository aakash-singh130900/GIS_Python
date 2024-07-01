import geopandas as gpd
import pandas as pd

# File paths
shapefile_path = r"C:/pythia/Simulation_Data_India/India/shapes/Sri_Lanka.shp"
excel_file_path = r"C:/Users/dell/Desktop/lat_lng.xlsx"
output_shapefile_path = r"C:/pythia/Simulation_Data_India/India/shapes/Updated_Sri_Lanka.shp"

# Read the shapefile using geopandas
gdf = gpd.read_file(shapefile_path)

# Read the Excel file using pandas
df = pd.read_excel(excel_file_path)

# Ensure the 'ID' column exists in both dataframes
if 'ID' not in gdf.columns or 'ID' not in df.columns:
    raise ValueError("The 'ID' column must exist in both the shapefile and the Excel file.")

# Merge the GeoDataFrame and DataFrame on the 'ID' column
merged_gdf = gdf.merge(df[['ID', 'Info_Weather']], on='ID')

# Save the merged GeoDataFrame back to a new shapefile
merged_gdf.to_file(output_shapefile_path)

print(f"Updated shapefile with new column successfully saved to {output_shapefile_path}")
