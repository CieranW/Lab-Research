from pprint import pprint
from data_operations import (
    scan_files,
    find_variable_locations_with_values,
    print_data_to_terminal,
    questions_and_actions,
    latest_version,
)


def main():
    # Sets the input and output directories
    input_directory = "input"
    output_directory = "output"
    alert_file = "TextFiles/alert.txt"
    # Notification system to update the user on the latest version and changes
    latest_version(alert_file)

    # Main dictionary to store data from each CSV file
    data_dict = scan_files()

    # Call the function to write the data to the output file
    variable_data = find_variable_locations_with_values(data_dict)

    # For testing purposes
    # print_data_to_terminal(variable_data, data_dict)
    # print("Contents of data_dict:")
    # pprint(data_dict)

    # print("\nContents of variable_data:")
    # pprint(variable_data)

    # Function to perform actions
    questions_and_actions(variable_data, data_dict, input_directory, output_directory)


if __name__ == "__main__":
    main()
