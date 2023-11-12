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


# TODO: modify this function to work with the alert.txt file, keeping track of updates and changes
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
    while True:
        # Print out each file name
        for filename in data_dict.keys():
            print(f"\nDataset: {filename}")
            print(f"Variables in {filename}:")
            for variable in data_dict[filename]:
                print(variable)

        print_options_from_file("TextFiles/modify_options.txt")
        option = int(
            input("Which option would you like to choose? (Enter the number): ")
        )
        if option == 1:
            modify_dataset(data_dict)
        elif option == 2:
            modify_dataset_variable(data_dict)
        elif option == 3:
            break


def modify_dataset(data_dict):
    while True:
        print_options_from_file("TextFiles/modify_dataset.txt")
        option = int(
            input("Which option would you like to choose? (Enter the number): ")
        )
        if option == 1:
            # Ask the user what they want to name the new dataset
            new_file = input("What would you like to name the new dataset?: ")
            # Check if the file already exists
            if new_file in data_dict:
                print("The file already exists.")
                continue
            else:
                # Check if the filename ends with ".csv". If not, add it to the end of the filename
                if new_file.endswith(".csv") is False:
                    new_file += ".csv"

                # Create a new key in the dictionary
                data_dict[new_file] = {}
                # Ask the user what variables they want to add to the new dataset
                new_variables = input(
                    "What variables would you like to add to the new dataset? (Enter the variable names separated by a comma): "
                )
                # Split the variables into a list
                new_variables = new_variables.split(", ")
                # Go through each new variable and add values to the list
                for variable in new_variables:
                    # Add the new variables to the dictionary
                    data_dict[new_file][variable] = []
                    # Ask the user what values they want to add to the list
                    new_values = input(
                        f"What values would you like to add to {variable}? (Enter the values separated by a comma): "
                    )
                    # Split the values into a list
                    new_values = new_values.split(", ")
                    # Convert the values to integers
                    new_values = [float(value) for value in new_values]
                    # Add the values to the list
                    data_dict[new_file][variable] = new_values

                # Print out the new file and variables
                print(f"New dataset: {new_file}")
                print(f"New variables in {new_file}:")
                for variable in data_dict[new_file]:
                    print(variable)
                print()
        elif option == 2:
            print()
            # Print out each dataset name
            for dataset in data_dict.keys():
                print(dataset)
            print()
            # Ask the user which file they want to remove
            remove_file = input(
                "Which dataset would you like to remove? (Enter the dataset): "
            )
            # Check if the file exists
            if remove_file in data_dict:
                # Remove the file from the dictionary
                data_dict.pop(remove_file)
                print(f"{remove_file} has been removed.")
            else:
                print("The file you entered does not exist.")
        elif option == 3:
            break


def modify_dataset_variable(data_dict):
    while True:
        print_options_from_file("TextFiles/modify_in_dataset.txt")
        option = int(
            input("which option would you like to choose? (Enter the number):")
        )
        # 1| Remove a variable from the list
        # 2| Remove a value from the list
        # 3| Add a new variable to the list
        # 4| Add a new value to the list
        # 5| Change a value in the list
        # 6| Change all values in the list
        # 7| Exit the process
        if option == 1:
            # Ask the user which file they want to modify
            remove_file = input(
                "Which dataset would you like to remove values from? (Enter the dataset): "
            )
            remove_variables = input(
                "Which variable would you like to remove? (Enter the variable name): "
            )
            # Print out the keys and values in the file
            if remove_file in data_dict and remove_variables in data_dict[remove_file]:
                # Remove the variable from the dictionary
                data_dict[remove_file].pop(remove_variables)
            else:
                print("The variable you entered does not exist.")

        elif option == 2:
            # Ask the user which file they want to modify
            remove_file = input(
                "Which dataset would you like to remove values from? (Enter the dataset): "
            )
            remove_variables = input(
                "Which variable would you like to remove values from? (Enter the variable name): "
            )
            # Print out the keys and values in the file
            if remove_file in data_dict and remove_variables in data_dict[remove_file]:
                print(f"Values in {remove_file}:")
                i = 1
                print(f"Index | {remove_variables}")
                for value in data_dict[remove_file][remove_variables]:
                    print(f"{i} | {value}")
                    i += 1
                # Ask the user which value they want to remove
                remove_index = int(
                    input(
                        "Which value would you like to remove? (Enter the index number): "
                    )
                )
                for value in data_dict[remove_file][remove_variables]:
                    # Check if the value is in the list
                    if (
                        data_dict[remove_file][remove_variables][remove_index - 1]
                        == value
                    ):
                        # Remove the value from the list
                        data_dict[remove_file][remove_variables].remove(value)
                        print(f"New values in {remove_file}:")
                        print(data_dict[remove_file][remove_variables])
                        break
                    else:
                        print("The value you entered is not in the dataset.")
        elif option == 3:
            # Ask the user which file they want to modify
            add_file = input(
                "Which dataset would you like to add values to? (Enter the dataset): "
            )
            add_variables = input(
                "Which variable would you like to add? (Enter the variable name): "
            )
            # Print out the keys and values in the file
            if add_file in data_dict:
                data_dict[add_file][add_variables] = []
                # Ask the user what values they want to add to the list
                new_values = input(
                    f"What values would you like to add to {add_variables}? (Enter the values separated by a comma): "
                )
                # Split the values into a list
                new_values = new_values.split(", ")
                # Convert the values to integers
                new_values = [float(value) for value in new_values]
                # Add the values to the list
                data_dict[add_file][add_variables] = new_values
                # Print out the new file and variables
                print(f"New variable in {add_file}: {add_variables}")
                print(data_dict[add_file][add_variables])

            else:
                print("The variable you entered does not exist.")
        elif option == 4:
            # Ask the user which file they want to modify
            add_file = input(
                "Which dataset would you like to add values to? (Enter the dataset): "
            )
            add_variables = input(
                "Which variable would you like to add values to? (Enter the variable name): "
            )
            # Print out the keys and values in the file
            if add_file in data_dict and add_variables in data_dict[add_file]:
                # Ask the user what values they want to add to the list
                new_values = input(
                    f"What values would you like to add to {add_variables}? (Enter the values separated by a comma): "
                )
                # Split the values into a list
                new_values = new_values.split(", ")
                # Convert the values to integers
                new_values = [float(value) for value in new_values]
                # Add the values to the list
                data_dict[add_file][add_variables].extend(new_values)
                # Print out the new file and variables
                print(f"New values in {add_file}:")
                print(data_dict[add_file][add_variables])
            else:
                print("The variable you entered does not exist.")
        elif option == 5:
            # Ask the user which file they want to modify
            access_file = input(
                "Which dataset would you like to access? (Enter the dataset): "
            )
            access_variables = input(
                "Which variable would you like to modify? (Enter the variable name): "
            )

            # Print out the keys and values in the file
            if access_file in data_dict and access_variables in data_dict[access_file]:
                print(f"Values in {access_file}:")
                i = 1
                print(f"Index | {access_variables}")
                for value in data_dict[access_file][access_variables]:
                    print(f"{i} | {value}")
                    i += 1
                # Ask the user which value they want to modify
                access_index = int(
                    input(
                        "Which value would you like to modify? (Enter the index number): "
                    )
                )
                for value in data_dict[access_file][access_variables]:
                    # Check if the value is in the list
                    if (
                        data_dict[access_file][access_variables][access_index - 1]
                        == value
                    ):
                        print(
                            f"Current value: {data_dict[access_file][access_variables][access_index - 1]}"
                        )
                        # Ask the user what they want to change the value to
                        new_value = float(
                            input("What would you like to change the value to?: ")
                        )
                        # Change the value in the list
                        data_dict[access_file][access_variables][
                            access_index - 1
                        ] = new_value
                        print(f"New values in {access_file}:")
                        print(data_dict[access_file][access_variables])
                        break
                    else:
                        print("The value you entered is not in the dataset.")

        elif option == 6:
            # Ask the user which file they want to modify
            access_file = input(
                "Which dataset would you like to access? (Enter the dataset): "
            )
            access_variables = input(
                "Which variable would you like to modify? (Enter the variable name): "
            )

            # Print out the keys and values in the file
            if access_file in data_dict and access_variables in data_dict[access_file]:
                print(f"Values in {access_file}:")
                i = 1
                print(f"Variable: {access_variables}")
                for value in data_dict[access_file][access_variables]:
                    print(f"{value}")
                    new_value = float(
                        input("What would you like to change the value to?: ")
                    )
                    # Change the value in the list
                    data_dict[access_file][access_variables][value] = new_value
                print(f"New values in {access_file}:")
                print(data_dict[access_file][access_variables])
            else:
                print("The variable you entered does not exist.")
        elif option == 7:
            break


# TODO: Implement a system to notify the user of the latest version and changes. Will be called at the start of the program or after each action
def latest_version():
    pass


def questions_and_actions(variable_data, data_dict, input_directory, output_directory):
    while True:
        latest_version()
        print_options_from_file("TextFiles/options.txt")
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
