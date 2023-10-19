import csv
import os


def read_csv(filename):
    data = {}  # Dictionary to store the data

    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)

        # Read the headers (first row)
        headers = next(reader)

        # Initialize the data dictionary with empty lists for each header
        for header in headers:
            data[header] = []

        # Read and store the data
        for row in reader:
            for i, value in enumerate(row):
                data[headers[i]].append(float(value))

    return data


def find_variable_locations_with_values(data_dict):
    # Initialize a dictionary to store variable locations and values
    variable_data = {}

    # Iterate through each file's data to collect unique variable names
    unique_variables = set()
    for data in data_dict.values():
        unique_variables.update(data.keys())

    # Initialize the variable data dictionary with the unique variable names
    for variable in unique_variables:
        variable_data[variable] = {"locations": [], "values": []}

    # Append the file names to each respective variable and store their values
    for filename, data in data_dict.items():
        for variable in unique_variables:
            if variable in data:
                variable_data[variable]["locations"].append(filename)
                variable_data[variable]["values"].append(data[variable])

    return variable_data


def print_data(data):
    for variable, values in data.items():
        print(f"{variable}: {values}")


def main():
    # Directory containing your CSV files
    directory = "DashBoardProject"  # Replace with the actual directory path

    # Create a dictionary to store data from each CSV file
    data_dict = {}

    # Iterate over all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            print(f"\nData from {filename}:")
            filepath = os.path.join(directory, filename)
            data = read_csv(filepath)
            print_data(data)
            # Store data in the dictionary with the filename as the key
            data_dict[filename] = data

    # Now you have data from all CSV files in data_dict for comparison or future use
    # For example, you can access data from a specific file using data_dict["filename.csv"]

    variable_data = find_variable_locations_with_values(data_dict)
    for var, data in variable_data.items():
        locations = ", ".join(data["locations"])
        print(f"\n{var} is found in: {locations}")
        for i, location in enumerate(data["locations"]):
            values = ", ".join(map(str, data["values"][i]))  # Convert values to strings
            print(f"{var} in {location}: {values}")


if __name__ == "__main__":
    main()
