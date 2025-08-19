import glob
from itertools import cycle

from util.convert_list.convert_list import split_list

files = glob.glob("**/test*.py",recursive=True)
print("Files found:", len(files))
pids = list(range(1, 4))  # Example PIDs for demonstration

chunk_size = len(pids)

chunk_list_data = split_list(files, chunk_size)

print(len(chunk_list_data), "chunks created with size:", chunk_size)
print(len(pids), "PIDs found:", pids)
for chunk, pid in zip(chunk_list_data, cycle(pids)):
    print(f"Processing file: {chunk} with PID: {pid}")
