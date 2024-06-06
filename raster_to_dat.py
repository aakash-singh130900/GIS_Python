import fiona
import rasterio
import datetime
from math import radians, cos, sin, sqrt, atan2

def read_shapefile(shapefile_path):
    points = []
    with fiona.open(shapefile_path, 'r') as shapefile:
        for feature in shapefile:
            geom = feature['geometry']
            if geom['type'] == 'Point':
                points.append((geom['coordinates'][1], geom['coordinates'][0]))  # (lat, lng)
            elif geom['type'] == 'Polygon':
                for coord in geom['coordinates'][0]:
                    points.append((coord[1], coord[0]))  # (lat, lng)
    return points

def get_raster_values_at_location(raster_paths, lat, lng):
    values = []
    for raster_path in raster_paths:
        try:
            with rasterio.open(raster_path) as src:
                coords = src.index(lng, lat)
                raster_value = src.read(1)[coords[1], coords[0]]
                if raster_value == src.nodata:
                    values.append(None)
                else:
                    values.append(raster_value)
        except Exception as e:
            values.append(None)
    return values

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def find_closest_valid_point(points, target_lat, target_lng, raster_values_list):
    min_distance = float('inf')
    closest_values = None
    for i, (lat, lng) in enumerate(points):
        if None not in raster_values_list[i]:
            distance = haversine_distance(target_lat, target_lng, lat, lng)
            if distance < min_distance:
                min_distance = distance
                closest_values = raster_values_list[i]
    return closest_values

def create_dat_file(dat_file_path, points, raster_values_list, parameter_names):
    try:
        with open(dat_file_path, 'w') as file:
            file.write("* General info about this file\n")
            file.write("*\n")
            file.write("* Contents      : Model data file\n")
            file.write("* Creator       : FST translator version 2.11\n")
            file.write("* Creation date : {:%d-%b-%Y, %H:%M:%S}\n".format(datetime.datetime.now()))
            file.write("* Source file   : WHEAT_UPLOAD_FINAL_2014.FST\n")
            file.write("*----------------------------------------------------------------------*\n\n")
            
            file.write("* contains:\n")
            file.write("* - Initial constants as far as specified with INCON statements,\n")
            file.write("* - Model parameters,\n")
            file.write("* - AFGEN/CSPLIN interpolation functions,\n")
            file.write("* - A SCALE array in case of a general translation\n\n")
            
            file.write("* Initial constants\n")
            file.write("* -----------------\n")
            for i in range(1, 12):
                file.write(f"DAT{i:<5} = {i}.0\n")
            file.write("\n")
            
            file.write("* Model parameters\n")
            file.write("* ----------------\n")
            for i, ((lat, lng), raster_values) in enumerate(zip(points, raster_values_list)):
                if None in raster_values:
                    raster_values = find_closest_valid_point(points, lat, lng, raster_values_list)
                    if raster_values is None:
                        continue  # Skip if no valid point found
                date = datetime.date(2010, 1, 1) + datetime.timedelta(days=i)
                file.write(f"* Parameters for {date:%Y-%m-%d}, Latitude: {lat}, Longitude: {lng}\n")
                for param_name, value in zip(parameter_names, raster_values):
                    file.write(f"{param_name:<8} = {value:.2f}\n")
                file.write("\n")
            file.write("*----------------------------------------------------------------------*\n")
        print(f"Data file successfully created at {dat_file_path}")
    except Exception as e:
        print(f"Error creating data file: {e}")

def main():
    shapefile_path = "C:/D/Soil/SHAPEFILE/pb_hr.shp"
    raster_paths = [
        "C:/D/Soil/Four_States/Cu_FourStates.tif",
        "C:/D/Soil/Four_States/EC_FourStates.tif",
        "C:/D/Soil/Four_States/Fe_FourStates.tif",
        "C:/D/Soil/Four_States/K_FourStates.tif",
        "C:/D/Soil/Four_States/Mn_FourStates.tif",
        "C:/D/Soil/Four_States/N_FourStates.tif",
        "C:/D/Soil/Four_States/OC_FourStates.tif",
        "C:/D/Soil/Four_States/P_FourStates.tif",
        "C:/D/Soil/Four_States/pH_FourStates.tif",
        "C:/D/Soil/Four_States/S_FourStates.tif",
        "C:/D/Soil/Four_States/Zn_FourStates.tif",
    ]
    parameter_names = [
        "Cu",
        "EC",
        "Fe",
        "K",
        "Mn",
        "N",
        "OC",
        "P",
        "pH",
        "S",
        "Zn",
    ]
    dat_file_path = "C:/D/Soil/data.dat"

    points = read_shapefile(shapefile_path)
    raster_values_list = [get_raster_values_at_location(raster_paths, lat, lng) for lat, lng in points]
    create_dat_file(dat_file_path, points, raster_values_list, parameter_names)

if __name__ == "__main__":
    main()
