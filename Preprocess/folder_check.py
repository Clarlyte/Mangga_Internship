import os
import fnmatch

def check_image_files_and_subdirectories(directory):
    second_to_last_folders = []
    
    # Loop through the top level directories
    for root, dirs, files in os.walk(directory):
        # Check if the current directory has subdirectories (i.e., it's not a last-level folder)
        if dirs:
            # Check if any of the subdirectories are last-level folders
            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                if os.path.isdir(subdir_path):
                    sub_subdirs = next(os.walk(subdir_path))[1]
                    if len(sub_subdirs) == 0:
                        # If there are no sub-subdirectories, it's a last-level folder
                        second_to_last_folders.append(root)
                        break
    
    # Remove duplicates from second-to-last folders list
    second_to_last_folders = list(set(second_to_last_folders))

    # Now check the last-level folders and the second-to-last directory
    for root, dirs, files in os.walk(directory):
        if not dirs:
            # Last-level folder: check the images
            jpg_images = fnmatch.filter(files, '*.jpg')
            png_images = fnmatch.filter(files, '*.png')
            total_images = len(jpg_images) + len(png_images)
            if total_images != 3:
                print(f"Folder '{root}' does NOT have exactly 3 angles of the Mango. It has {total_images} images.")
                
    for second_to_last_folder in second_to_last_folders:
        if len(next(os.walk(second_to_last_folder))[1]) != 4:
            print(f"This image '{second_to_last_folder}' does NOT have exactly 4 sides. It has {len(next(os.walk(second_to_last_folder))[1])} recorded sides.")
        
# Specify the directory to start the search
root_directory = r'D:\AI internship\Field Image Data raw\July 20 Bogo 105 DAFI'

# Run the check
check_image_files_and_subdirectories(root_directory)
