# from Model import Model
# import numpy as np
# import matplotlib.pyplot as plt
#
# mdl = Model(12, 12, 100, '06/05/1999') # why is az vertical in the middle of the day? # it inverts after 0 deg
# #mdl = Model(34.42,-119.82, 6200, '2019-12-06')
#
# mdl.trim() # trim the plots to one full cycle of apparent_elevation
# #mdl.show_plots()
#
# mdl.show_plots()
#
# arr = mdl.get_dni_arr()
# print(arr)
# print(np.multiply(arr, .38))

import json

FILEPATH = "data/history.json"

def save_to_file(lat, lon, elevation, date, speaker_color):
    print("Saving to file")
    arr = []
    new_element = {
        "name": "Recent #1",
        "latitude": lat,
        "longitude": lon,
        "elevation": elevation
    }
    try:
        with open(FILEPATH, 'r') as data:
            print("[jsonhelper] Read data file")
            arr = json.load(data)
    except:
        print("[jsonhelper] File does not exist, creating it")

    arr.insert(0, new_element)

    # trim the array to 5 elements max
    if len(arr) > 5:
        arr = arr[0:5]

    # Set names
    for i in range(0, len(arr)):
        arr[i]["name"] = "Recent 1 - lat:" + str(int(lat)) + ", lon:" + str(int(lon))

    # Save
    try:
        with open(FILEPATH, 'w') as outfile:
            json.dump(arr, outfile)
            print("[jsonhelper] File saved to", FILEPATH)
    except:
        print("[jsonhelper] Unable to write to file at", FILEPATH)

def get_history_arr():
    try:
        with open(FILEPATH, 'r') as data:
            return json.load(data)
    except:
        print("[jsonhelper] Unable to read history json")

save_to_file(5, 6, 7, 8, "black")

print(get_history_arr())
