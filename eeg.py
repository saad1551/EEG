import pandas as pd
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

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


















































# def process_all_files():
#     files = listdir('raw_data/csv/SW & SSW CSV Files')
#     print(f"\n\n{len(files)} files found")

#     dfs = []

#     for file in files:
#         df = pd.read_csv(f'raw_data/csv/SW & SSW CSV Files/{file}')
#         dfs.append(df)

#     if dfs:
#         concatenated_df = pd.concat(dfs, ignore_index=True)
#         print(concatenated_df.values.tolist())




# def parse_timestamp(timestamp):
#     # If timestamp does not contain milliseconds, append ':00'
#     if ':' in timestamp and len(timestamp.split(':')) == 3:
#         timestamp += ':00'
    
#     # Split timestamp into hours, minutes, seconds, and milliseconds
#     hours, minutes, seconds, milliseconds = map(int, timestamp.split(':'))
    
#     # Create datetime.time object
#     time_obj = datetime.strptime(f"{hours}:{minutes}:{seconds}.{milliseconds}", "%H:%M:%S.%f").time()
    
#     return time_obj


# df = pd.read_csv('raw_data/csv/SW & SSW CSV Files/1020.csv')

# file = df.values.tolist()

# all_events = set()

# for index, row in df.iterrows():
#     channel_name = row['Channel names']
#     comment = row['Comment']
#     all_events.add((channel_name, comment))

# events = list(all_events)

# print(f"{len(events)} distinct events found in the recording\n\n")

# for event in events:
#     count = 0
#     total_time = 0
#     for row in file:
#         # Find event occurence
#         if row[-2] == event[0] and row[-1] == event[1]:
#             count += 1
#             start = row[3]
#             end = row[4]

#             # Parse timestamps
#             start = parse_timestamp(start)
#             end = parse_timestamp(end)

#             # Calculate difference
#             time_difference = datetime.combine(datetime.min, end) - datetime.combine(datetime.min, start)
#             event_time = time_difference.total_seconds()

#             # Add to the total event time
#             total_time += event_time

#     # Print event details
#     print(f"Event: {event[0]}, {event[1]}")
#     print(f"# Occurences: {count}")
#     print(f"Average duration: {total_time / count:.4f} seconds\n")




# print(f"\n\nTotal occurences: {len(file)}")



# import matplotlib.pyplot as plt
# import pandas as pd
# from matplotlib.colors import ListedColormap

# # Sample data loading (replace with your actual data loading logic)
# data = {
#     'Start time': ['10:22:01.052', '10:22:10.295', '10:22:12.026', '10:22:13.043', '10:23:14.791',
#                    '10:23:17.052', '10:23:22.086', '10:23:25.443', '10:24:03.043', '10:24:10.026',
#                    '10:24:10.043', '10:24:21.034', '10:25:03.660', '10:25:07.660', '10:25:08.991'],
#     'End time': ['10:22:05.947', '10:22:11.965', '10:22:12.956', '10:22:14.965', '10:23:16.765',
#                  '10:23:21.686', '10:23:24.417', '10:23:26.000', '10:24:03.947', '10:24:10.460',
#                  '10:24:10.513', '10:24:22.965', '10:25:07.260', '10:25:08.591', '10:25:10.006'],
#     'Channel names': ['FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'O1 O2',
#                       'T5 T6',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ',
#                       'FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ PZ CZ']
# }

# # Convert to DataFrame
# df = pd.DataFrame(data)

# # Convert time strings to numerical values for easier plotting
# def time_to_sec(time_str):
#     h, m, s = map(float, time_str.split(':'))
#     return h * 3600 + m * 60 + s

# df['Start_sec'] = df['Start time'].apply(time_to_sec)
# df['End_sec'] = df['End time'].apply(time_to_sec)

# # Create a mapping from channel names to their positions (y-axis indices)
# channel_names = df['Channel names'].str.split().explode().unique()
# channel_map = {channel: i for i, channel in enumerate(channel_names)}

# # Create a heatmap plot
# fig, ax = plt.subplots(figsize=(15, 8))

# # Define colormap
# cmap = ListedColormap(['white', 'red'])  # Red for events, white for non-events

# # Plot each event as a colored rectangle in the heatmap
# for index, row in df.iterrows():
#     start = row['Start_sec']
#     end = row['End_sec']
#     channel_names = row['Channel names'].split()
#     for channel in channel_names:
#         y = channel_map[channel]
#         ax.fill_betweenx([y - 0.4, y + 0.4], start, end, color='red', alpha=0.3)

# # Adjust y-axis ticks and labels
# ax.set_yticks(range(len(channel_names)))
# ax.set_yticklabels(channel_names, fontsize=8)

# # Set labels and title
# ax.set_xlabel('Time (seconds)', fontsize=12)
# ax.set_title('EEG Data Visualization', fontsize=14)

# # Add colorbar
# im = ax.imshow([[0, 1]], cmap=cmap, aspect='auto')
# fig.colorbar(im)

# # Display the plot
# plt.tight_layout()
# plt.show()