import mne
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import date
from matplotlib.patches import Rectangle

MAX_CHANNELS = 30
TIME_WINDOW = 5 #seconds
MIN_RECTANGLE_WIDTH = 0.5
RECTANGLE_HEIGHT = 0.8


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

# Load EEG data
raw = mne.io.read_raw_edf("D:/EEGData/raw_data/edf/Abnormal EDF Files/0000137.edf", preload=True)

channel_mapping = {}

for i in range(len(raw.info['ch_names'])):
    channel_mapping[raw.info['ch_names'][i]] = i

# Load CSV data
df = pd.read_csv("D:/EEGData/raw_data/csv/SW & SSW CSV Files/137.csv")

# list of dicts to contain events
events = []

# iterate through the rows of the dataframe
for index, row in df.iterrows():
    # make a list of channel names in each row
    channel_names = row['Channel names'].split()
    if isinstance(row['File Start'], str):
        file_start = row['File Start']
    event = {
        "channel_idxs": [channel_mapping[channel_name] for channel_name in channel_names],
        "channel_names": channel_names,
        "start_time": (parse_timestamp(row['Start time']) - parse_timestamp(file_start)).total_seconds(),
        "end_time": (parse_timestamp(row['Start time']) - parse_timestamp(file_start)).total_seconds(),
        "start_idx": raw.time_as_index((parse_timestamp(row['Start time']) - parse_timestamp(file_start)).total_seconds())[0],
        "end_idx": raw.time_as_index((parse_timestamp(row['End time']) - parse_timestamp(file_start)).total_seconds())[0] 
    }
    events.append(event)


# Plot raw data using MNE's raw.plot() with specified parameters
fig = raw.plot(duration=TIME_WINDOW, scalings=dict(eeg=1e-6), n_channels=MAX_CHANNELS, block=True, show=False)

# Access the matplotlib Axes object from the figure
ax = fig.get_axes()[0]

for event in events:
    for channel_idx in event['channel_idxs']:
        # Calculate coordinates and size of the rectangle
        rect_x = event['start_time'] - (MIN_RECTANGLE_WIDTH / 4)  # x-coordinate (start position)
        rect_y = channel_idx - (RECTANGLE_HEIGHT / 2) # center of y-axis minus half of rect_height
        rect_width = MIN_RECTANGLE_WIDTH + event['end_time'] - event['start_time'] # width of the rectangle
        rect_height = RECTANGLE_HEIGHT  # height of the rectangle

        # Create a rectangle patch
        rect = Rectangle((rect_x, rect_y), rect_width, rect_height, linewidth=1, edgecolor='b', facecolor='none')

        # Add the rectangle to the plot
        ax.add_patch(rect)

# Add a text annotation
ax.text(100, 0, 'Annotation', color='blue', fontsize=12)

# Customize further using matplotlib functions
ax.set_title('Customized Raw Data Plot')

# Display the plot (manually handle figure display due to MNE's backend)
plt.show()
