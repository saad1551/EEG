import pandas as pd
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os
import numpy as np
import matplotlib.pyplot as plt


RANDOM_EVENT_STATISTICS_TO_DISPLAY = 10
FILE_TO_STORE_ALL_EVENT_STATISTICS = "all_files_stats.csv"

def parse_timestamp(timestamp):
    # If timestamp does not contain milliseconds, append ':00'
    if ':' in timestamp and len(timestamp.split(':')) == 3:
        timestamp += ':00'
    
    # Split timestamp into hours, minutes, seconds, and milliseconds
    hours, minutes, seconds, milliseconds = map(int, timestamp.split(':'))
    
    # Create datetime.time object
    time_obj = datetime.strptime(f"{hours}:{minutes}:{seconds}.{milliseconds}", "%H:%M:%S.%f").time()
    
    return time_obj

def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        selected_file_label.config(text=f"Selected File: {file_path}")
        process_file(file_path)

def process_file(file_path):
    try:
        df = pd.read_csv(file_path)

        file = df.values.tolist()

        all_events = set()

        for index, row in df.iterrows():
            channel_name = row['Channel names']
            comment = row['Comment']
            all_events.add((channel_name, comment))

        events = list(all_events)

        print(f"{len(events)} distinct event(s) found in the recording\n\n")

        for event in events:
            count = 0
            total_time = 0
            for row in file:
                # Find event occurence
                if row[-2] == event[0] and row[-1] == event[1]:
                    count += 1
                    start = row[3]
                    end = row[4]

                    # Parse timestamps
                    start = parse_timestamp(start)
                    end = parse_timestamp(end)

                    # Calculate difference
                    time_difference = datetime.combine(datetime.min, end) - datetime.combine(datetime.min, start)
                    event_time = time_difference.total_seconds()

                    # Add to the total event time
                    total_time += event_time

            # Print event details
            print(f"Event: {event[0]}, {event[1]}")
            print(f"# Occurences: {count}")
            if count > 1:
                print(f"Average duration: {total_time / count:.4f} seconds\n")
            else:
                print(f"duration: {total_time:.4f} seconds\n")


        print(f"\n\nTotal occurences: {len(file)}\n\n")

    except Exception as e:
        selected_file_label.config(text=f"Error: {str(e)}")

def process_all_files(directory="D:/EEGData/raw_data/csv/SW & SSW CSV Files"):
    try:
        files = os.listdir(directory)

        all_files = []

        for file in files:
            file_path = os.path.join(directory, file)
            

            df = pd.read_csv(file_path)

            all_files.extend(df.values.tolist())

        all_events = set()

        for row in all_files:
            channel_name = row[-2]
            comment = row[-1]
            all_events.add((channel_name, comment))

        events = list(all_events)

        print(f"{len(events)} distinct events found in the recordings\n\n")

        random_indices = np.random.randint(0, len(events), RANDOM_EVENT_STATISTICS_TO_DISPLAY, dtype=int)

        print("Individual statistics of 10 randomly selected events computed over the entire dataset are shown below\n\n")

        event_statistics = []

        total_duration_of_all_events = 0

        avg_durations_of_all_events = []

        for index, event in enumerate(events):
            count = 0
            total_time = 0
            for row in all_files:
                # Find event occurence
                if row[-2] == event[0] and row[-1] == event[1]:
                    count += 1
                    start = row[3]
                    end = row[4]

                    # Parse timestamps
                    start = parse_timestamp(start)
                    end = parse_timestamp(end)

                    # Calculate difference
                    time_difference = datetime.combine(datetime.min, end) - datetime.combine(datetime.min, start)
                    event_time = time_difference.total_seconds()

                    # Add to the total event time
                    total_time += event_time

            avg_duration = round(total_time / count, 4)

            event_dict = {
                'Channel_names': event[0],
                'Comment': event[1],
                'total_time': round(total_time, 4),
                'occurences': count,
                'avg_duration': avg_duration
            }

            avg_durations_of_all_events.append(avg_duration)

            total_duration_of_all_events += total_time

            event_statistics.append(event_dict)

            if index in random_indices:
            # # Print event details
                print(f"Event: {event[0]}, {event[1]}")
                print(f"# Occurences: {count}")
                if count >= 1:
                    print(f"Average duration: {avg_duration} seconds\n")


        print(f"Total occurences in the dataset: {len(all_files)}\n\n")

        print(f"Average duration of all the events: {round(total_duration_of_all_events / len(all_files), 3)}\n")

        df = pd.DataFrame.from_records(event_statistics)

        df.to_csv(FILE_TO_STORE_ALL_EVENT_STATISTICS)

        print(f"Statistics of all the events saved to file {FILE_TO_STORE_ALL_EVENT_STATISTICS}")

        plt.figure(figsize=(10, 6))
        plt.hist(avg_durations_of_all_events, bins=10, edgecolor='black')
        plt.title('Histogram of Average Durations for All Abnormalities in the Dataset')
        plt.xlabel('Average Duration (seconds)')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()



    except Exception as e:
        selected_file_label.config(text=f"Error: {str(e)}")



# Main tkinter GUI setup
root = tk.Tk()
root.title("EEG Processing")

open_button = tk.Button(root, text="Open File", command=open_file_dialog)
open_button.pack(padx=20, pady=20)

all_files_button = tk.Button(root, text="Process All Files", command=process_all_files)
all_files_button.pack(padx=20, pady=20)

tk.Button(root, text="Quit", command=root.destroy).pack()

selected_file_label = tk.Label(root, text="Selected File:")
selected_file_label.pack()

file_text = tk.Text(root, wrap=tk.WORD, height=10, width=40)
file_text.pack(padx=20, pady=20)

root.mainloop()