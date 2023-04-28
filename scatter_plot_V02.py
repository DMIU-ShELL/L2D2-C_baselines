import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.markers as mmarkers

def read_csv_files(main_folder):
    all_files = []
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if file.endswith(".csv") and "train-log" in file:
                all_files.append(os.path.join(root, file))
    return all_files

from datetime import timedelta

from datetime import datetime

def create_scatter_plot(data, colors, markers):
    plt.figure(figsize=(15, 10))
    seen_labels = set()  # Keep track of labels that have been added to the legend
    
    msg_type_codes = {0: "IDQ", 1: "QR", 2: "MR", 3: "MTR"}
    marker = markers[0]  # Use the same marker shape for all experiments

    min_Timestamp = min([datetime.strptime(t, "%Y-%m-%d %H:%M:%S") for experiment in data for t in experiment['Timestamp']])
    
    for i, experiment in enumerate(data):
        # Filter rows where the 'Number' value is greater than 3
        experiment = experiment[experiment['Number'] <= 3]
        
        for msg_type, group in experiment.groupby('Number'):
            if len(group) > 0:
                color = colors.get(msg_type, 'gray')  # Use a default color (gray) if msg_type is not in the colors dictionary
                if msg_type not in colors:
                    print(f"Warning: Unknown message type {msg_type} encountered. Using gray as the default color.")
                msg_code = msg_type_codes.get(msg_type, "Unknown")
                label = f"Msg Type {msg_code}"
                if label not in seen_labels:
                    seen_labels.add(label)
                    # Convert string to datetime, subtract the minimum Timestamp, convert to seconds, and plot it
                    plt.scatter([(datetime.strptime(t, "%Y-%m-%d %H:%M:%S") - min_Timestamp).total_seconds() for t in group['Timestamp']], [i] * len(group), c=color, marker=marker, label=label, alpha=0.8)
                else:
                    plt.scatter([(datetime.strptime(t, "%Y-%m-%d %H:%M:%S") - min_Timestamp).total_seconds() for t in group['Timestamp']], [i] * len(group), c=color, marker=marker, alpha=0.8)

    plt.xlabel('Time (seconds)')
    plt.ylabel('Experiments')
    plt.title('Scatter Plot of Timestamps by Experiment and Message Type')
    
    if seen_labels:  # Check if any labels have been added to the legend
        plt.legend()
    
    plt.savefig('scatter_plot_LATEST.png', format='png', dpi=300)  # Save the plot as a PNG image with 300 dpi resolution
    plt.show()












def main():
    main_folder = 'C:/Users/chper/OneDrive - Loughborough University/CoLLA_Paper_Preparation/Agent_Communication_Data_Plots/data/75_dropout/75_dropout/seed_4'
    csv_files = read_csv_files(main_folder)

    all_data = [pd.read_csv(file, nrows=300) for file in csv_files]

    colors = {
        0: 'yellow',
        1: 'red',
        2: 'blue',
        3: 'green',
        # Add more colors for additional message types if needed
    }

    markers = list(mmarkers.MarkerStyle.markers.keys())
    markers = [m for m in markers if m not in ['.', ',']]  # Exclude '.' and ',' as they are too small

    create_scatter_plot(all_data, colors, markers)

if __name__ == "__main__":
    main()
