import json

FILEPATH = "data/history.json"

def save_history_to_file(lat, lon, elevation):
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
        arr[i]["name"] = "Recent " + str(i + 1) +" - lat:" + str(arr[i]["latitude"]) + ", lon:" + str(arr[i]["longitude"])

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