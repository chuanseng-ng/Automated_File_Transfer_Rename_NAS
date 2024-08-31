import os
import time
import argparse
import textwrap
import file_move.file_move as file_move_def
import user_input.user_input as user_input_def

parser = argparse.ArgumentParser(description="Script to automatically transfer files from specified source directory to indicated destination directory", 
                                 usage="Run python main.py -h for more info", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-s", "--source_dir", type=str, required=True, help=textwrap.dedent('''
Source directory path
Accepts both relative and absolute paths
Type = str'''))
parser.add_argument("-d", "--dest_dir",   type=str, required=True, help=textwrap.dedent('''
Destination directory path
Accepts both relative and absolute paths
Type = str'''))

args = parser.parse_args()

source_dir    = os.path.abspath(args.source_dir)
dest_base_dir = os.path.abspath(args.dest_dir)

start_time = time.time()

# From user-defined dict/list/str
name_pattern_dict = user_input_def.user_define_dict()

missing_dir_list = file_move_def.file_move_main(source_dir, dest_base_dir, name_pattern_dict)

# Report missing destination directories if any
if missing_dir_list:
    print("Missing destination directories:")
    for missing in missing_dir_list:
        print(missing)
    
    print("Check above-mentioned files and do manual move!")
    print("Refine name_pattern_dict to include mentioned files!")
else:
    # Echo completion message
    print("All files processed!")

end_time = time.time()

duration_sec = end_time - start_time

if duration_sec//60 != 0:
    duration_min = duration_sec/60
    if duration_min//60 != 0:
        duration = duration_min/60
        tag = "hr"
    else:
        duration = duration_min
        tag = "min"
else:
    duration = duration_sec
    tag = "sec"

print(f"Process took {duration} {tag} to finish!")