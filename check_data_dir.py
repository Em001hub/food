import os
import json
from datetime import datetime

# Check what's in the data directory
data_dir = 'data'
if os.path.exists(data_dir):
    print(f"Contents of {data_dir} directory:")
    files = os.listdir(data_dir)
    for file in files:
        print(f"  {file}")
        
        # If it's a JSON file, let's see what's in it
        if file.endswith('.json'):
            file_path = os.path.join(data_dir, file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    print(f"    Content: {data}")
            except Exception as e:
                print(f"    Error reading file: {e}")
else:
    print(f"{data_dir} directory does not exist")