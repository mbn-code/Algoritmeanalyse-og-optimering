import json
import csv
import os

def json_to_csv(input_filename, output_filename):
    # Open and load the JSON data from the input file
    with open(input_filename, 'r') as infile:
        json_data = json.load(infile)

    # Extract the traceEvents from the JSON data
    trace_events = json_data.get("traceEvents", [])

    # If there are no trace events, exit
    if not trace_events:
        print("No trace events found in the JSON data.")
        return

    # Get the header from the keys of the first trace event
    header = trace_events[0].keys()

    # Write the data to the CSV file
    with open(output_filename, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=header)

        # Write the header to the CSV file
        writer.writeheader()

        # Write each trace event to the CSV file
        for event in trace_events:
            writer.writerow(event)

    print(f"CSV file '{output_filename}' has been created.")

# Example usage
input_path = os.path.join('src_visualize', 'results.json')
output_path = os.path.join('src_visualize', 'results.csv')

json_to_csv(input_path, output_path)
