import json
import os
import tempfile
import heapq

def sort_and_save_to_temp_file(data, temp_file):
    # Sort the data by 'epoch' and then by 'nanoseconds'
    data.sort(key=lambda x: (x.get('instant').get('epochSecond'), x.get('instant').get('nanoOfSecond')))
    
    with open(temp_file, 'w') as f:
        json.dump(data, f)

def merge_sorted_files(temp_files, output_file):
    with open(output_file, 'a') as outfile:
        # outfile.write('[')  # Start of JSON array
        first_entry = True
        # Create a heap to manage the merging of sorted files
        # outfile.seek(-1,-1)
        heap = []
        file_handlers = [open(f, 'r') for f in temp_files]
        # Initialize the heap with the first object from each temp file
        for i, f in enumerate(file_handlers):
            line = f.readline()
            if line:
                data = json.loads(line)
                heapq.heappush(heap, (data, i))
        while heap:
            smallest_entry, file_index = heapq.heappop(heap)
            if first_entry:
                outfile.writelines(json.dumps(smallest_entry))
                first_entry = False
            else:
                # outfile.write(',' + json.dumps(smallest_entry))
                outfile.writelines(json.dumps(smallest_entry))
            # Read the next entry from the same temp file
            next_line = file_handlers[file_index].readline()
            if next_line:
                next_data = json.loads(next_line)
                heapq.heappush(heap, (next_data, file_index))
        # outfile.write(']')  # End of JSON array
    # Close all file handlers
    for f in file_handlers:
        f.close()

def merge_and_sort_large_json_files(input_files, output_file):
    temp_files = []
    try:
        # Read each input file in chunks
        for file in input_files:
            with open(file, 'r') as f:
                chunk_data = []
                for line in f:
                    if line.strip():  # Ignore empty lines
                        chunk_data.append(json.loads(line))
                    # If chunk is large enough, process and save to temp file
                    if len(chunk_data) >= 10000:  # Adjust chunk size as needed
                        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                            sort_and_save_to_temp_file(chunk_data, temp_file.name)
                            temp_files.append(temp_file.name)
                        chunk_data = []
                # Process any remaining data
                if chunk_data:
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        sort_and_save_to_temp_file(chunk_data, temp_file.name)
                        temp_files.append(temp_file.name)
        # Merge all sorted temporary files
        merge_sorted_files(temp_files, output_file)    
    except Exception as e:
        print(e)
        print(e.__traceback__)
        print(e.with_traceback())
    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            os.remove(temp_file)

if __name__ == "__main__":
    # List of input JSON files to be merged
    input_files = [file for file in os.listdir() if '.json' in file]
    print(input_files)
    output_file = 'merged_sorted_output.json'  # Output file name

    merge_and_sort_large_json_files(input_files, output_file)
