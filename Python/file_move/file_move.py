import os
import re
import shutil

def file_move_main(source_dir, dest_base_dir, name_pattern_dict):
    # List all MKV files in source directory
    files = [f for f in os.listdir(source_dir) if f.endswith('.mkv')]

    # Echo initial message
    print(f"Found {len(files)} MKV files to process")

    # List to keep track of missing destination directories
    missing_dir_list = []

    # Iterate through each file
    for file in files:
        file_path = os.path.join(source_dir, file)
        print(f"Processing file: {file_path}")

        # Extract file name without extension
        file_name = os.path.splitext(file)[0]

        # Extract pattern between "]" and "-"
        pattern_mid = re.sub(r'^.*?\] ', '', file_name)
        pattern_fin = re.sub(r' - [0-9].*$', '', pattern_mid)

        # Further extract season name if exists
        if re.search(r'S[0-9]', pattern_fin):
            pattern_mid = re.sub(r'^.*?\] ', '', file_name)
            pattern_fin = re.sub(r' S[0-9].*$', '', pattern_mid)

        # Define destination directory based on pattern
        dest_dir = os.path.join(dest_base_dir, pattern_fin)

        # Check if destination directory exists
        if not os.path.exists(dest_dir):
            dir_dict_found = False

            for key, value in name_pattern_dict:
                if pattern_fin in key:
                    dest_dir       = os.path.join(dest_base_dir, value)
                    dir_dict_found = True
            
            if dir_dict_found:
                print(f"Destination directory exists, found in dict: {dest_dir}")
            else:
                missing_dir_list.append(pattern_fin)
                print(f"Destination directory does not exist: {pattern_fin}")
        else:
            print(f"Destination directory exists: {dest_dir}")

            # Check if sub-directories exists
            sub_dirs = [d for d in os.listdir(dest_dir) if os.path.isdir(os.path.join(dest_dir, d))]

            if not sub_dirs:
                # Move file into main directory
                shutil.move(file_path, dest_dir)
                print(f"Moved file - {file} - to main directory: {dest_dir}\n")
            else:
                # Determine highest season number
                highest_season = 0

                for dir in sub_dirs:
                    match = re.match(r'Season (\d+)', dir)
                    if match:
                        season_number = int(match.group(1))
                        if season_number > highest_season:
                            highest_season = season_number
            
                # Update destination directory with highest season number
                dest_dir = os.path.join(dest_dir, f"Season {highest_season}")

                # Move file to sub-directory with highest season number
                shutil.move(file_path, dest_dir)
                print(f"Moved file - {file} - to sub-directory: {dest_dir}\n")

    return missing_dir_list