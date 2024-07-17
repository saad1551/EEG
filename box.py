import mne
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import date

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
raw = mne.io.read_raw_edf("D:/EEGData/raw_data/edf/Abnormal EDF Files/0000956.edf", preload=True)

channel_mapping = {}

for i in range(len(raw.info['ch_names'])):
    channel_mapping[raw.info['ch_names'][i]] = i + 1

# Load CSV data
df = pd.read_csv("D:/EEGData/raw_data/csv/SW & SSW CSV Files/956.csv")

# list of dicts to contain events
events = []

# iterate through the rows of the dataframe
for index, row in df.iterrows():
    # make a list of channel names in each row
    channel_names = row['Channel names'].split()
    if isinstance(row['File Start'], str):
        file_start = row['File Start']
    event = {
        "channel_names": channel_names,
        "start_time": (parse_timestamp(row['Start time']) - parse_timestamp(file_start)).total_seconds(),
        "end_time": (parse_timestamp(row['End time']) - parse_timestamp(file_start)).total_seconds() 
    }
    events.append(event)
    # iterate through the list of channel names
    # for channel_name in channel_names:
    #     # make a dictionary of an event
    #     event = {
    #         "channel_name": channel_name,
    #         "start_time": (parse_timestamp(row['Start time']) - parse_timestamp(file_start)).total_seconds(),
    #         "end_time": (parse_timestamp(row['End time']) - parse_timestamp(file_start)).total_seconds() 
    #     }
    #     # add it to the list
    #     events.append(event)



onset = [event['start_time'] for event in events]
duration = [(event['end_time'] - event['start_time']) for event in events]
description = [' '.join(event['channel_names']) for event in events]

# Define your annotations including channel names
annotations = mne.Annotations(onset=onset, duration=duration, description=description)

raw.set_annotations(annotations)

raw.plot(duration=5, n_channels = 30, block=True)  # Get current figure

