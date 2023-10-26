import csv
import os
import pandas as pd
from pprint import pprint


def scan_files():
    input_directory = "newData"
    # Create a dictionary to store data from each CSV file
    data_dict = {}

    # Iterate over all CSV files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(input_directory, filename)
            data = read_csv(filepath)
            # Store data in the dictionary with the filename as the key
            data_dict[filename] = data

    return data_dict


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
                # Strip whitespace from the value
                stripped_value = value.strip()
                # Append the stripped value to the respective list
                data[headers[i]].append(float(stripped_value))

    return data


def find_variable_locations_with_values(data_dict):
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


def write_variable_data_to_file(variable_data, output_file, data_dict):
    with open(output_file, "w") as file:
        # Output data from each CSV file first
        for variable, values in data_dict.items():
            file.write(f"{variable}\n")
            for var, var_data in values.items():
                var_values = ", ".join(map(str, var_data))
                file.write(f"{var}: {var_values}\n")
            file.write("\n")

        # Then, output the variable data for each variable
        for var, data in variable_data.items():
            locations = ", ".join(data["locations"])
            file.write(f"\n{var} is found in: {locations}\n")

            for i, location in enumerate(data["locations"]):
                values = ", ".join(map(str, data["values"][i]))
                file.write(f"{var} in {location}: {values}\n")


def print_data_to_terminal(variable_data, data_dict):
    # Output data from each CSV file first
    for variable, values in data_dict.items():
        print(f"{variable}")
        for var, var_data in values.items():
            var_values = ", ".join(map(str, var_data))
            print(f"{var}: {var_values}")

        print("\n")

    # Then, output the variable data for each variable
    for var, data in variable_data.items():
        locations = ", ".join(data["locations"])
        print(f"{var} is found in: {locations}")

        for i, location in enumerate(data["locations"]):
            values = ", ".join(map(str, data["values"][i]))
            print(f"{var} in {location}: {values}")

        print("\n")


def format_and_save(input_directory, output_directory):
    all_files = [f for f in os.listdir(input_directory) if f.endswith(".csv")]

    for input_file in all_files:
        data = pd.read_csv(os.path.join(input_directory, input_file))
        output_file = os.path.join(
            output_directory, input_file
        )  # Set the full output path
        data.to_csv(output_file, header=True, index=False)


def compare_data(data_dict1, data_dict2):
    # Find common variables in both data dictionaries
    common_variables = set(data_dict1.keys()) & set(data_dict2.keys())

    # Create dictionaries to store the differences
    differences_in_data_dict1 = {}
    differences_in_data_dict2 = {}

    # Compare data in common variables
    for variable in common_variables:
        if data_dict1[variable] != data_dict2[variable]:
            differences_in_data_dict1[variable] = data_dict1[variable]
            differences_in_data_dict2[variable] = data_dict2[variable]

    return differences_in_data_dict1, differences_in_data_dict2


def compare():
    input_directory = "newData"
    output_directory = "oldData"

    # Create dictionaries to store data from each location
    data_dict1 = {}
    data_dict2 = {}

    # Iterate over all CSV files in the first directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(input_directory, filename)
            data = read_csv(filepath)
            # Store data in the dictionary with the filename as the key
            data_dict1[filename] = data

    # Iterate over all CSV files in the second directory
    for filename in os.listdir(output_directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(output_directory, filename)
            data = read_csv(filepath)
            # Store data in the dictionary with the filename as the key
            data_dict2[filename] = data

    print("Data Differences Between Locations:")
    differences1, differences2 = compare_data(data_dict1, data_dict2)

    print("\nDifferences in Location 1:")
    pprint(differences1)

    print("\nDifferences in Location 2:")
    pprint(differences2)


def main():
    # Sets the input and output directories
    input_directory = "newData"
    output_directory = "oldData"

    # Output file name
    output_file = "output.txt"

    # Main dictionary to store data from each CSV file
    data_dict = scan_files()

    # Call the function to write the data to the output file
    variable_data = find_variable_locations_with_values(data_dict)
    write_variable_data_to_file(variable_data, output_file, data_dict)
    print_data_to_terminal(variable_data, data_dict)

    # For testing purposes
    # print("Contents of data_dict:")
    # pprint(data_dict)

    # print("\nContents of variable_data:")
    # pprint(variable_data)

    # Call the function to compare the data
    compare()

    # After performing the comparison, format and save the data
    format_and_save(input_directory, output_directory)


if __name__ == "__main__":
    main()
