import csv
import os
from tqdm import tqdm
import concurrent.futures

def process_csv_file(file_path, output_suffix='_output.csv'):
    # Initialize a dictionary to store the count of unique message types
    message_counts = {}

    # Read the input .csv file
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            message_type = int(row['Number'])
            if message_type in message_counts:
                message_counts[message_type] += 1
            else:
                message_counts[message_type] = 1

    # Write the results to a new .csv file in the same folder
    output_file_path = os.path.splitext(file_path)[0] + output_suffix
    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for message_type, count in message_counts.items():
            writer.writerow({'ID': message_type, 'Count': count})

    return file_path, message_counts

def get_all_csv_files(directory, csv_files=None):
    if csv_files is None:
        csv_files = []

    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith('.csv') and 'train-log' in entry.name and '_output' not in entry.name:
            csv_files.append(entry.path)
        elif entry.is_dir():
            get_all_csv_files(entry.path, csv_files)

    return csv_files

input_directory = 'new_data_b/95_dropout_seed_1'  # Replace with the path to your main directory
average_output_file = os.path.join(input_directory, 'average_message_type_counts.csv')

# Initialize a dictionary to store the aggregated count of unique message types
aggregated_counts = {}

# Get the list of all .csv files to process
csv_files = get_all_csv_files(input_directory)

# Process the .csv files in parallel using a process pool
with concurrent.futures.ProcessPoolExecutor() as executor:
    # Initialize a progress bar
    with tqdm(total=len(csv_files), desc="Processing .csv files") as progress_bar:
        # Process the .csv files and update the progress bar when each one is finished
        for file_path, message_counts in executor.map(process_csv_file, csv_files):
            progress_bar.update(1)

            # Aggregate the counts
            for message_type, count in message_counts.items():
                if message_type in aggregated_counts:
                    aggregated_counts[message_type] += count
                else:
                    aggregated_counts[message_type] = count

# Calculate the average count for each message type
average_counts = {message_type: count / len(csv_files) for message_type, count in aggregated_counts.items()}

# Write the average counts to a new .csv file in the main folder
with open(average_output_file, 'w', newline='') as csvfile:
    fieldnames = ['ID', 'Average Count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for message_type, average_count in average_counts.items():
        writer.writerow({'ID': message_type, 'Average Count': average_count})

print(f"Average counts written to {average_output_file}")
