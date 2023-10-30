import csv
import os
import pandas as pd
from pprint import pprint


def scan_files():
    input_directory = "input"
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


# Do we need this function?
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

    # Then, output the variable data for each variable along with the locations and values
    for var, data in variable_data.items():
        locations = ", ".join(data["locations"])
        print(f"{var} is found in: {locations}")

        for i, location in enumerate(data["locations"]):
            values = ", ".join(map(str, data["values"][i]))
            print(f"{var} in {location}: {values}")

        print("\n")


# Save the latest version of the data in the output directory
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


def modify_data(data_dict):
    # Print out each file name
    for filename in data_dict.keys():
        print(f"Filename: {filename}")
        # Now, you can loop through the variables in the current file (if needed)
        print(f"Variables in {filename}:")
        for variable in data_dict[filename]:
            print(variable)
        print()

    # Ask the user which file they want to modify
    access_file = input("Which file would you like to access? (Enter the file name): ")
    access_variables = input(
        "Which variable would you like to modify? (Enter the variable name): "
    )

    # Print out the keys and values in the file
    if access_file in data_dict and access_variables in data_dict[access_file]:
        print(f"Values in {access_file}:")
        i = 1
        for value in data_dict[access_file][access_variables]:
            print(f"{i}: {value}")
            i += 1
        print(data_dict[access_file][access_variables])
        # Ask the user which value they want to modify
        access_index = int(
            input("Which value would you like to modify? (Enter the index number): ")
        )
        # TODO: Figure out if we're accessing the index of the actual value itself. The index might be the smarter choice so perhaps we print out the index number alongside the values in the list. Then, we can ask the user which index they want to modify. Accessing and changing the values from there shouldn't be a problem. Additionally, we can add a check to see if the user entered a valid index number or if they would like to add a value to the list (a simple apend). We can also add a check to see if the user wants to remove a value from the list (a simple remove). We can also add a check to see if the user wants to change the entire list (a simple reassignment).
        for value in data_dict[access_file][access_variables]:
            # TODO: Accessing the variable within the value list now works. Next step is figuring out how to change the value of the variables and then write the changes to the file. Additionally, are we changing all the values or just one, adding or removing a value, or changing the entire list?
            # TODO: write another option file specifically for the modifying data function. This will allow the user to choose what they want to do with the data. They can change the entire list, change one value, add a value, or remove a value.
            if data_dict[access_file][access_variables][access_index - 1] == value:
                # Ask the user what they want to change the value to
                new_value = input("What would you like to change the value to?: ")
                # Find the index of the value in the list
                index = data_dict[access_file][access_variables].index(access_index - 1)
                # Change the value in the list
                data_dict[access_file][access_variables][index] = new_value
                print(f"New values in {access_file}:")
                print(data_dict[access_file][access_variables])
            else:
                print("The value you entered is not in the file.")
        # Check if the value is in the list
        if access_index in data_dict[access_file][access_variables]:
            # Ask the user what they want to change the value to
            new_value = input("What would you like to change the value to?: ")
            # Find the index of the value in the list
            index = data_dict[access_file][access_variables].index(access_index)
            # Change the value in the list
            data_dict[access_file][access_variables][index] = new_value
            print(f"New values in {access_file}:")
            print(data_dict[access_file][access_variables])
        else:
            print("The value you entered is not in the file.")

    else:
        print("The value you entered is not in the file.")


# TODO: Implement a system to notify the user of the latest version and changes. Will be called at the start of the program or after each action
def latest_version():
    pass


def questions_and_actions(variable_data, data_dict, input_directory, output_directory):
    while True:
        latest_version()
        print_options_from_file("options.txt")
        question = input("What would you like to do? ")
        if question == "4":
            format_and_save(input_directory, output_directory)
            break
        elif question == "1":
            print_data_to_terminal(variable_data, data_dict)
        elif question == "2":
            modify_data(data_dict)
        elif question == "3":
            compare()


def print_options_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) < 2:
                print(
                    "Invalid file format. The file should contain at least two lines."
                )
                return

            # Extract headers
            header_line = lines[1].strip()
            headers = header_line.split("|")

            # Print headers
            print("\nOptions:")
            print("-", "|", "-" * len(headers[1]))

            # Extract and print option lines
            for line in lines[1:]:
                option_number, option_description = line.split("|")
                print(option_number.strip(), "|", option_description.strip())

            # Print footer
            print("-", "|", "-" * len(headers[1]), "\n")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
