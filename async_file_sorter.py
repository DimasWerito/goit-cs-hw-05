import argparse
import asyncio
import os
from pathlib import Path
import shutil
import logging

# Configure logging to log errors
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file_path, target_dir):
    """Asynchronously copy a file to the target directory based on file extension."""
    try:
        # Extract file extension and create a target subdirectory based on it
        extension = file_path.suffix.lstrip('.').lower() or 'unknown'
        destination_dir = target_dir / extension
        destination_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy file to the new destination
        destination_file = destination_dir / file_path.name
        await asyncio.to_thread(shutil.copy, file_path, destination_file)
        print(f"Copied {file_path} to {destination_file}")
        
    except Exception as e:
        logging.error(f"Failed to copy {file_path}: {e}")

async def read_folder(source_dir, target_dir):
    """Recursively read all files in the source folder and process them."""
    tasks = []
    try:
        for root, _, files in os.walk(source_dir):
            for file_name in files:
                file_path = Path(root) / file_name
                tasks.append(copy_file(file_path, target_dir))
        
        # Run all copy tasks asynchronously
        await asyncio.gather(*tasks)
    
    except Exception as e:
        logging.error(f"Error reading folder {source_dir}: {e}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Sort files by extension into subfolders.")
    parser.add_argument("source_folder", type=str, help="Path to the source folder containing files.")
    parser.add_argument("output_folder", type=str, help="Path to the destination folder for sorted files.")
    args = parser.parse_args()
    
    # Set up paths
    source_dir = Path(args.source_folder)
    target_dir = Path(args.output_folder)
    
    # Run the async file sorting
    asyncio.run(read_folder(source_dir, target_dir))

if __name__ == "__main__":
    main()
