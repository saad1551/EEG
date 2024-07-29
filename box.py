import mne
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import date
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import filedialog

MAX_CHANNELS = 30
TIME_WINDOW = 5 #seconds
MIN_RECTANGLE_WIDTH = 0.5
RECTANGLE_HEIGHT = 0.6
EEG_SCALING = 1e-6


def parse_timestamp(timestamp):
    # If timestamp does not contain milliseconds, append ':00'
    if ':' in timestamp and len(timestamp.split(':')) == 3:
        timestamp += ':00'
    
    # Split timestamp into hours, minutes, seconds, and milliseconds
    hours, minutes, seconds, _ = map(int, timestamp.split(':'))

    _, _, _, milliseconds = map(str, timestamp.split(':'))
    
    # Create datetime.time object
    time_obj = datetime.strptime(f"{hours}:{minutes}:{seconds}.{milliseconds}", "%H:%M:%S.%f").time()
    
    return datetime.combine(date.today(), time_obj)


def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select an EDF File", filetypes=[("EDF files", "*.edf")])
    if file_path:
        selected_file_label.config(text=f"Selected File: {file_path}")
        process_file(file_path)

def process_file(file_path):
    try:
        csv_index = int(file_path.split('/')[-1].split('.')[0])

        # Load CSV data
        df = pd.read_csv(f"D:/EEGData/raw_data/csv/SW & SSW CSV Files/{csv_index}.csv")

        # Load EEG data
        raw = mne.io.read_raw_edf(file_path, preload=True)

        channel_mapping = {}

        for i in range(len(raw.info['ch_names'])):
            channel_mapping[raw.info['ch_names'][i]] = i

        # Define custom colors for comments
        color_map = {
            'delta slow waves': 'red',
            'sharp and slow wave': 'blue',
            'spike and wave': 'green',
            
            # Add more events and their corresponding colors here
        }

        # list of dicts to contain events
        events = []

        # iterate through the rows of the dataframe
        for index, row in df.iterrows():
            # make a list of channel names in each row
            channel_names = row['Channel names'].split()
            comment = row['Comment']
            color = color_map.get(comment, 'black')  # Default to black if the comment is not in color_map

            if isinstance(row['File Start'], str):
                file_start = row['File Start']
            event = {
                "channel_idxs": [channel_mapping[channel_name] for channel_name in channel_names],
                "channel_names": channel_names,
                "start_time": (parse_timestamp(row['Start time']) - parse_timestamp(file_start)).total_seconds(),
                "end_time": (parse_timestamp(row['Start time']) - parse_timestamp(file_start)).total_seconds(),
                "color": color
            }
            events.append(event)


        # Plot raw data using MNE's raw.plot() with specified parameters
        fig = raw.plot(duration=TIME_WINDOW, scalings=dict(eeg=EEG_SCALING), n_channels=MAX_CHANNELS, block=True, show=False)

        # Access the matplotlib Axes object from the figure
        ax = fig.get_axes()[0]

        for event in events:
            for channel_idx in event['channel_idxs']:
                # Calculate coordinates and size of the rectangle
                rect_x = max(0.01, event['start_time'] - (MIN_RECTANGLE_WIDTH / 4)) # x-coordinate (start position)
                rect_y = channel_idx - (RECTANGLE_HEIGHT / 2) # y ordinate (start position)
                rect_width = MIN_RECTANGLE_WIDTH + event['end_time'] - event['start_time'] # width of the rectangle
                rect_height = RECTANGLE_HEIGHT  # height of the rectangle

                # Create a rectangle patch
                rect = Rectangle((rect_x, rect_y), rect_width, rect_height, linewidth=1, edgecolor=event['color'], facecolor='none')

                # Add the rectangle to the plot
                ax.add_patch(rect)

        ax.set_title('Customized Raw Data Plot')

        plt.show()

    except FileNotFoundError:
        selected_file_label.config(text="Error: Corresponding CSV file does not exist. Please try another recording")

    except Exception as e:
        selected_file_label.config(text=f"Error: {str(e)}")


# Main tkinter GUI setup
root = tk.Tk()
root.title("EEG Processing")

open_button = tk.Button(root, text="Open File", command=open_file_dialog)
open_button.pack(padx=20, pady=20)

tk.Button(root, text="Quit", command=root.destroy).pack()

selected_file_label = tk.Label(root, text="Selected File:")
selected_file_label.pack()

file_text = tk.Text(root, wrap=tk.WORD, height=10, width=40)
file_text.pack(padx=20, pady=20)

root.mainloop()