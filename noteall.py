#from note_rpa import main_play
from note_rpa_pkl import main_play
from dotenv import load_dotenv
import os
import glob
import time

# Load the environment variables from .env
load_dotenv()

# Get the directory path from the VOICE_DIR environment variable
voice_dir = os.environ.get("VOICE_DIR")

# Check if VOICE_DIR is not None
if voice_dir:
    # Create a pattern to match all .mp3 files in the directory
    pattern = os.path.join(voice_dir, '*.mp3')
    
    # Use glob to get a list of .mp3 file paths
    mp3_files = glob.glob(pattern)
    
    # Sort the list in place
    mp3_files.sort()
else:
    print("VOICE_DIR environment variable is not set or is empty.")
    mp3_files = []

# mp3_files now contains a sorted list of .mp3 file paths from VOICE_DIR
for mp3_file in mp3_files:
    # Define the .done filename
    done_file = f"{mp3_file}.done"
    
    # Check if the .done file already exists
    if os.path.exists(done_file):
        print(f"Skipping {mp3_file}, .done file already exists.")
        continue

    # If the .done file does not exist, process the mp3 file
    print(f"Processing {mp3_file}")
    main_play(mp3_file, "apply")
    
    # Create a .done file to indicate the mp3 has been processed
    open(done_file, 'a').close()
    print(f"Created empty file: {done_file}")

    time.sleep(5)

