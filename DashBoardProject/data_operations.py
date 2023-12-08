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
def format_and_save(data_dict, output_directory):
    for file_name, data in data_dict.items():
        with open(f"{output_directory}/{file_name}", "w") as file:
            if not data:  # If the dictionary for a file is empty, skip writing it
                continue

            headers = ",".join(data.keys())
            file.write(headers + "\n")

            # Transpose the data matrix to iterate over rows instead of columns
            rows = zip(*data.values())

            for row in rows:
                row_values = ",".join(str(value) for value in row)
                file.write(row_values + "\n")


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
    input_directory = "input"
    output_directory = "output"

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
        print("\nCurrent datasets:")
        # Print out each file name
        for filename in data_dict.keys():
            print(f"\nDataset: {filename}")
            print(f"Variables in {filename}:")
            for variable in data_dict[filename]:
                print(f"{variable}: {data_dict[filename][variable]}")

        print_options_from_file("TextFiles/modify_options.txt")
        option = int(
            input("Which option would you like to choose? (Enter the number): ")
        )
        # 1| Modify a dataset
        if option == 1:
            modify_dataset(data_dict)
        # 2| Modify a variable in a dataset
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

        # 1| Add a dataset
        if option == 1:
            # Ask the user what they want to name the new dataset
            new_file = input("What would you like to name the new dataset?: ")
            # Check if the filename ends with ".csv". If not, add it to the end of the filename
            if new_file.endswith(".csv") is False:
                new_file += ".csv"
            # Check if the file already exists
            if new_file in data_dict:
                print("The file already exists.")
                continue
            else:
                # Create a new key in the dictionary
                data_dict[new_file] = {}

                add_variable = input("Would you like to add variables now? (Y/N): ")
                if add_variable == "Y":
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
                    print(f"\nNew dataset: {new_file}")
                    print(f"New variables in {new_file}:")
                    for variable in data_dict[new_file]:
                        print(variable)
                    print()

                    # Update the alert file with the most recent changes
                    message = "Added a new dataset, " + new_file + " to the database."
                    alert(message)

                else:
                    print(f"\nNew dataset: {new_file}")
                    print(f"New variables in {new_file}:")
                    print("No variables added yet.")
                    print()

                    # Update the alert file with the most recent changes
                    message = (
                        "Added a new dataset, "
                        + new_file
                        + " to the database, did not add any variables."
                    )
                    alert(message)

                # Display all the current datasets
                print("Current datasets:")
                for filename in data_dict.keys():
                    print(filename)

        # 2| Remove a dataset
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

            # Check if the filename ends with ".csv". If not, add it to the end of the filename
            if remove_file.endswith(".csv") is False:
                remove_file += ".csv"

            # Check if the file exists
            if remove_file in data_dict:
                # Remove the file from the dictionary
                data_dict.pop(remove_file)
                print(f"{remove_file} has been removed.")

                # Display all the current datasets
                print("Current datasets:")
                for filename in data_dict.keys():
                    print(filename)

                # Update the alert file with the most recent changes
                message = "Removed " + remove_file + " from the database."
                alert(message)
            else:
                print("The file you entered does not exist.")

        # 3| Exit the process
        elif option == 3:
            break


def modify_dataset_variable(data_dict):
    while True:
        print_options_from_file("TextFiles/modify_in_dataset.txt")
        option = int(
            input("Which option would you like to choose? (Enter the number):")
        )
        # 7| Exit the process
        if option == 7:
            break
        else:
            # Print out each file name for the user to choose
            for filename in data_dict.keys():
                print(filename)

            # Ask the user which file they want to modify
            modify_file = input(
                "Which dataset would you like to modify? (Enter the dataset): "
            )
            # Check if the filename ends with ".csv". If not, add it to the end of the filename
            if modify_file.endswith(".csv") is False:
                modify_file += ".csv"

            # Print out the keys and values in the file
            if modify_file in data_dict:
                print(f"Variables in {modify_file}:")
                for variable in data_dict[modify_file]:
                    print(variable)

            # 1| Remove a variable from the list
            if option == 1:
                # Ask the user which variable they want to remove
                remove_variables = input(
                    "Which variable would you like to remove? (Enter the variable name): "
                )

                if (
                    modify_file in data_dict
                    and remove_variables in data_dict[modify_file]
                ):
                    # Remove the variable from the dictionary
                    data_dict[modify_file].pop(remove_variables)

                    # Update the alert file with the most recent changes
                    message = (
                        "Removed " + remove_variables + " from " + modify_file + "."
                    )
                    alert(message)

                else:
                    print("The variable you entered does not exist.")

            # 2| Remove a value from the list
            elif option == 2:
                # Ask the user which variable they want to remove values from
                remove_variables = input(
                    "Which variable would you like to remove values from? (Enter the variable name): "
                )

                # Print out the keys and values in the file
                if (
                    modify_file in data_dict
                    and remove_variables in data_dict[modify_file]
                ):
                    print(f"Values in {modify_file}:")
                    print(f"Index | {remove_variables}")
                    for i, value in enumerate(
                        data_dict[modify_file][remove_variables], start=1
                    ):
                        print(f"{i} | {value}")

                    # Ask the user which value they want to remove
                    remove_index = int(
                        input(
                            "Which value would you like to remove? (Enter the index number): "
                        )
                    )

                    for value in data_dict[modify_file][remove_variables]:
                        # Check if the value is in the list
                        if (
                            data_dict[modify_file][remove_variables][remove_index - 1]
                            == value
                        ):
                            # Remove the value from the list
                            data_dict[modify_file][remove_variables].remove(value)
                            print(f"New values in {modify_file}:")
                            print(data_dict[modify_file][remove_variables])

                            # Update the alert file with the most recent changes
                            message = (
                                "Removed "
                                + str(value)
                                + " from "
                                + remove_variables
                                + " located in "
                                + modify_file
                                + "."
                            )
                            alert(message)
                            break
                        else:
                            print("The value you entered is not in the dataset.")

            # 3| Add a new variable to the list
            elif option == 3:
                # Ask the user which variable they want to add values to
                add_variables = input(
                    "Which variable would you like to add? (Enter the variable name): "
                )
                # Print out the keys and values in the file
                if modify_file in data_dict:
                    data_dict[modify_file][add_variables] = []
                    # Ask the user what values they want to add to the list
                    new_values = input(
                        f"What values would you like to add to {add_variables}? (Enter the values separated by a comma): "
                    )
                    # Split the values into a list
                    new_values = new_values.split(", ")
                    # Convert the values to integers
                    new_values = [float(value) for value in new_values]
                    # Add the values to the list
                    data_dict[modify_file][add_variables] = new_values
                    # Print out the new file and variables
                    print(f"New variable in {modify_file}: {add_variables}")
                    print(data_dict[modify_file][add_variables])

                    # Update the alert file with the most recent changes
                    message = (
                        "Added a new variable, "
                        + add_variables
                        + " to "
                        + modify_file
                        + "."
                    )
                    alert(message)
                else:
                    print("The variable you entered does not exist.")

            # 4| Add a new value to the list
            elif option == 4:
                # Ask the user which variable they want to add values to
                add_variables = input(
                    "Which variable would you like to add values to? (Enter the variable name): "
                )
                # Print out the keys and values in the file
                if modify_file in data_dict and add_variables in data_dict[modify_file]:
                    # Ask the user what values they want to add to the list
                    new_values = input(
                        f"What values would you like to add to {add_variables}? (Enter the values separated by a comma): "
                    )
                    # Split the values into a list
                    new_values = new_values.split(", ")
                    # Convert the values to integers
                    new_values = [float(value) for value in new_values]
                    # Add the values to the list
                    data_dict[modify_file][add_variables].extend(new_values)
                    # Print out the new file and variables
                    print(f"New values in {modify_file}:")
                    print(data_dict[modify_file][add_variables])

                    # Update the alert file with the most recent changes
                    message = (
                        "Added new values to "
                        + add_variables
                        + ", located in "
                        + modify_file
                        + "."
                    )
                    alert(message)
                else:
                    print("The variable you entered does not exist.")

            # 5| Change a value in the list
            elif option == 5:
                # Ask the user which variable they want to modify
                access_variables = input(
                    "Which variable would you like to modify? (Enter the variable name): "
                )

                # Print out the keys and values in the file
                if (
                    modify_file in data_dict
                    and access_variables in data_dict[modify_file]
                ):
                    print(f"Values in {modify_file}:")
                    i = 1
                    print(f"Index | {access_variables}")
                    for value in data_dict[modify_file][access_variables]:
                        print(f"{i} | {value}")
                        i += 1
                    # Ask the user which value they want to modify
                    access_index = int(
                        input(
                            "Which value would you like to modify? (Enter the index number): "
                        )
                    )
                    for value in data_dict[modify_file][access_variables]:
                        # Check if the value is in the list
                        if (
                            data_dict[modify_file][access_variables][access_index - 1]
                            == value
                        ):
                            print(
                                f"Current value: {data_dict[modify_file][access_variables][access_index - 1]}"
                            )
                            # Ask the user what they want to change the value to
                            new_value = float(
                                input("What would you like to change the value to?: ")
                            )
                            # Change the value in the list
                            data_dict[modify_file][access_variables][
                                access_index - 1
                            ] = new_value
                            print(f"New values in {modify_file}:")
                            print(data_dict[modify_file][access_variables])

                            # Update the alert file with the most recent changes
                            message = (
                                "Changed the value of "
                                + str(value)
                                + " to "
                                + str(new_value)
                                + " in "
                                + modify_file
                                + "."
                            )
                            alert(message)
                            break

            # 6| Change all values in the list
            elif option == 6:
                # Ask the user which variable they want to modify
                access_variables = input(
                    "Which variable would you like to modify? (Enter the variable name): "
                )

                # Print out the keys and values in the file
                if (
                    modify_file in data_dict
                    and access_variables in data_dict[modify_file]
                ):
                    print(f"Values in {modify_file}:")
                    i = 1
                    print(f"Variable: {access_variables}")
                    # Change the value in the list
                    for idx, value in enumerate(
                        data_dict[modify_file][access_variables]
                    ):
                        print(f"{value}")
                        new_value = float(
                            input("What would you like to change the value to?: ")
                        )
                        # Change the value in the list using the index
                        data_dict[modify_file][access_variables][idx] = new_value
                    print(f"New values in {modify_file}:")
                    print(data_dict[modify_file][access_variables])

                    # Update the alert file with the most recent changes
                    message = (
                        "Changed the values of "
                        + access_variables
                        + " in "
                        + modify_file
                        + "."
                    )
                    alert(message)
                else:
                    print("The variable you entered does not exist.")


# TODO: Implement a system to notify the user of the latest version and changes. Will be called at the start of the program or after each action
def latest_version(alert_file):
    # Read the file, line by line and add each line to a list
    with open(alert_file, "r") as file:
        lines = file.readlines()

        # Reverse the list so the latest version is at the top
        lines.reverse()

        # Print out the latest version and changes
        print("Most Recent Updates and Changes:")
        for i, line in enumerate(lines[:5], start=1):
            print(f"{i}| {line}")  # strip() removes the newline character


# TODO: modify this function to work with the alert.txt file, keeping track of updates and changes
def alert(alert_message):
    alert_file = "TextFiles/alert.txt"
    with open(alert_file, "a") as file:
        # Add the new alert to the file
        file.write(alert_message + "\n")


# To view specific datasets
def print_specific_dataset(data_dict):
    # Print the keys of the data_dict
    print("Available datasets:")
    for key in data_dict.keys():
        print(key)

    user_input_key = input("Which dataset would you like to view?")

    # Check if the dataset has ".csv" at the end
    if not user_input_key.endswith(".csv"):
        user_input_key += ".csv"
    # Check if the user-input key exists in the data_dict
    if user_input_key in data_dict:
        values = data_dict[user_input_key]
        print(f"{user_input_key}")
        for var, var_data in values.items():
            var_values = ", ".join(map(str, var_data))
            print(f"{var}: {var_values}")
        print("\n")
    else:
        print(f"The key '{user_input_key}' does not exist in the dictionary.")


def questions_and_actions(variable_data, data_dict, input_directory, output_directory):
    while True:
        print_options_from_file("TextFiles/options.txt")
        question = int(input("What would you like to do? "))
        # 1| Print data to terminal
        # 2| Modify data
        # 3| Display differences between databases
        # 4| View a dataset
        # 5| Show latest changes
        # 6| Quit and save changes
        if question == 6:
            format_and_save(data_dict, output_directory)
            break
        elif question == 1:
            print_data_to_terminal(variable_data, data_dict)
        elif question == 2:
            modify_data(data_dict)
        elif question == 3:
            compare()
        elif question == 4:
            print_specific_dataset(data_dict)
        elif question == 5:  # TODO: Check again.
            latest_version("TextFiles/alert.txt")


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
