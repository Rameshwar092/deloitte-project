import json
from datetime import datetime

# git This function takes an ISO-formatted date (like "2023-06-01T08:30:00.000Z")
# and converts it into milliseconds (used in the final unified format)
def iso_to_millis(iso_str):
    dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S.%fZ")  # Convert string to datetime
    millis = int(dt.timestamp() * 1000)  # Convert to milliseconds
    return millis

#  This function processes data from 'data-1.json'
# That file already has timestamps in milliseconds, but field names are different
def transform_data_1(input_data):
    transformed = []
    for entry in input_data:
        transformed.append({
            "device_id": entry["deviceId"],     # Rename "deviceId" to "device_id"
            "timestamp": int(entry["timestamp"]),  # Already in milliseconds
            "temperature": entry["temp"],       # Rename "temp" to "temperature"
            "humidity": entry["hum"]            # Rename "hum" to "humidity"
        })
    return transformed

# This function processes data from 'data-2.json'
# This file uses ISO-formatted timestamps and different field names
def transform_data_2(input_data):
    transformed = []
    for entry in input_data:
        transformed.append({
            "device_id": entry["id"],                      # Rename "id" to "device_id"
            "timestamp": iso_to_millis(entry["time"]),     # Convert "time" from ISO to ms
            "temperature": entry["temperature"],           # Already correct field name
            "humidity": entry["humidity"]                  # Already correct field name
        })
    return transformed

#  This is the main part of the script that runs everything
if _name_ == "_main_":
    # Load the JSON data from both input files
    with open("data-1.json") as f1:
        data1 = json.load(f1)
    with open("data-2.json") as f2:
        data2 = json.load(f2)

    #  Convert each format to the standard format
    result1 = transform_data_1(data1)
    result2 = transform_data_2(data2)

    #  Combine the two lists into one
    final_result = result1 + result2

    #  Save the combined data into the output file
    with open("data-result.json", "w") as f_out:
        json.dump(final_result, f_out, indent=2)  # Pretty print with indent

    #  Confirmation message
    print(" Transformation complete. Output saved in 'data-result.json'")