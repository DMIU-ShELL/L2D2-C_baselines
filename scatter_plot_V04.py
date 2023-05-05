import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.markers as mmarkers

def load_data(folder_path):
    all_data = []
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if "train-log" in file and file.endswith(".csv"):
                file_path = os.path.join(subdir, file)
                data = pd.read_csv(file_path)  # Read only the first 300 rows
                all_data.append(data)
    return all_data


from datetime import timedelta

from datetime import datetime

import random

def jitter(value, amount=0.1):
    return value + random.uniform(-amount, amount)

import random
import matplotlib.patches as mpatches

def create_scatter_plot(all_data, colors, markers):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot()

    #plt.figure(figsize=(15, 10))
    seen_labels = set()  # Keep track of labels that have been added to the legend

    msg_type_codes = {0: "IDQ", 1: "QR", 2: "MR", 3: "MTR"}
    marker = markers[0]  # Use the same marker shape for all experiments

    min_Timestamp = min([datetime.strptime(t, "%Y-%m-%d %H:%M:%S") for experiment in all_data for t in experiment['Timestamp']])

    unique_msg_types = set()
    unique_msg_types = set()
    for i, experiment in enumerate(all_data):
        experiment = experiment[experiment['Number'] <= 3]
        for msg_type, group in experiment.groupby('Number'):
            unique_msg_types.add(msg_type)
            color = colors.get(msg_type, 'gray')
            jitter = [random.uniform(-0.1, 0.1) for _ in range(len(group))]
            plt.scatter([(datetime.strptime(t, "%Y-%m-%d %H:%M:%S") - min_Timestamp).total_seconds() for t in group['Timestamp']],
                        [i + 1 + j for j in jitter], c=color, marker=marker, alpha=0.8)

    # Create custom legend
    legend_handles = [mpatches.Patch(color=colors[msg_type], label=f'Msg Type: {msg_type_codes[msg_type]}') for msg_type in unique_msg_types]
    ax.legend(handles=legend_handles, title='Message Types', loc='upper left',  borderaxespad=0.)

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Agent')
    plt.xticks(rotation=45)
    plt.yticks(range(1, 13))
    plt.grid(True)
    plt.title('Agent Communication Scatter Plot')
    plt.tight_layout()
    plt.savefig('scatter_plot_new_data_75_dropout_seed_1d.png')
    plt.show()















def main():
    main_folder = 'C:/Users/chper/OneDrive - Loughborough University/CoLLA_Paper_Preparation/Agent_Communication_Data_Plots/new_data_b/75_dropout_seed_1/seed_1'
    #csv_files = read_csv_files(main_folder)

    all_data = load_data(main_folder)
    print(all_data)
    print(type(all_data))
    print(len(all_data))
    print(type(all_data[0]))
    print(len(all_data[0]))
    

    #all_data = [pd.read_csv(file) for file in csv_files]

    colors = {
        0: 'orange',
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
