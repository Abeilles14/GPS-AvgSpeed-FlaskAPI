# client for GPS coordinates, calculates speed
import requests
import time
import utm
import json
import math

# api-endpoint
URL = "http://127.0.0.1:5000/coordinates"
response = requests.get(URL)

if response.status_code == 200:
    # decode json object to list of dicts
    coord_list = json.loads(response.content.decode('utf-8'))
else:
    exit("Error in accessing data, check server connection.")

# number of coords
lines = len(coord_list)
line_count = 1;

is_first_coord = True

for coord in coord_list:
    dd_coord = coord.split()

    # convert to utm (easting and northing measurements)
    utm_coord = utm.from_latlon(float(dd_coord[0]), float(dd_coord[1]))

    if is_first_coord == True:
        original_easting_utm = utm_coord[0]
        original_northing_utm = utm_coord[1]
        last_easting_utm = utm_coord[0]
        last_northing_utm = utm_coord[1]

        is_first_coord = False

    current_easting_utm = utm_coord[0]
    current_northing_utm = utm_coord[1]

    # instantaneous displacement
    easting_displacement = current_easting_utm - last_easting_utm
    northing_displacement = current_northing_utm - last_northing_utm

    # instantaneous speed: sqrt(d1^2 +d2^2)/t, t = 1 sec
    inst_speed = round(math.sqrt((easting_displacement**2 + northing_displacement**2)),4)

    # average displacement
    easting_displacement = current_easting_utm - original_easting_utm
    northing_displacement = current_northing_utm - original_northing_utm

    # average speed: sqrt(d1^2 +d2^2)/t, t = 1 sec
    avg_speed = round(math.sqrt((easting_displacement**2 + northing_displacement**2)) / line_count, 4)

    print("utm coord: {}, inst speed: {}, avg speed: {}".format(utm_coord, inst_speed, avg_speed))

    last_easting_utm = current_easting_utm
    last_northing_utm = current_northing_utm

    line_count += 1;

    time.sleep(1)