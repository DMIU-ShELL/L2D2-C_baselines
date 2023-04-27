import os
import pandas as pd
import matplotlib.pyplot as plt

main_folder_path = "C:/Users/chper/OneDrive - Loughborough University/CoLLA_Paper_Preparation/Agent_Communication_Data_Plots/data/75_dropout/75_dropout"
colors = ['red', 'green', 'blue', 'yellow', 'orange']
shapes = ['o', 's', '^', 'D', '*']
fig, ax = plt.subplots()
for i, (folder_path, subfolders, file_names) in enumerate(os.walk(main_folder_path)):
    for file_name in file_names:
        if file_name.endswith('.csv') and 'train-log' in file_name:
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            #print(df.head(5))
            x = pd.to_datetime(df['Timestamp'])
            y = [i] * len(x)
            c = [colors[int(number) % len(colors)] for number in df['Number']]
            m = shapes[i % len(shapes)]
            ax.scatter(x, y, c=c, marker=m)
plt.savefig('scatter_plot.png')