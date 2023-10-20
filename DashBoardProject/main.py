import csv
import os
from pprint import pprint


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


def main():
    # Directory containing your CSV files
    directory = "DashBoardProject"  # Replace with the actual directory path

    # Create a dictionary to store data from each CSV file
    data_dict = {}

    # Iterate over all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            data = read_csv(filepath)
            # Store data in the dictionary with the filename as the key
            data_dict[filename] = data

    # Output file name
    output_file = "output.txt"

    # Call the function to write the data to the output file
    variable_data = find_variable_locations_with_values(data_dict)
    write_variable_data_to_file(variable_data, output_file, data_dict)

    print("Contents of data_dict:")
    pprint(data_dict)

    print("\nContents of variable_data:")
    pprint(variable_data)


if __name__ == "__main__":
    main()