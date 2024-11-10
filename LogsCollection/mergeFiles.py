import os
import json
import heapq

parentFolder = os.getcwd()

fileName = "logs.txt"
file_handlers = [open(file, 'r') for file in os.listdir(parentFolder) if '.txt' in file]

# Use a heap to efficiently merge sorted data
with open(os.path.join(parentFolder, fileName), 'w') as output:
    # Initialize a heap with the first line from each file
    heap = []
    for i, f in enumerate(file_handlers):
        line = f.readline()
        try:
            line = json.load(line)
            heapq.heappush(heap, (line, i))
        except Exception as e:
            print(e)

    while heap:
        # Get the smallest line from the heap
        smallest_line, file_index = heapq.heappop(heap)
        output.write(smallest_line)
        # Read the next line from the same file
        next_line = file_handlers[file_index].readline()
        if next_line:
            heapq.heappush(heap, (next_line, file_index))

# Close all file handlers
for f in file_handlers:
    f.close()

print(f"Data merged and sorted into {os.path.join(parentFolder, fileName)}.")

