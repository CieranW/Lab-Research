from data_operations import (
    scan_files,
    find_variable_locations_with_values,
    write_variable_data_to_file,
    print_data_to_terminal,
    format_and_save,
    compare,
)


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
