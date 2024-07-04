import os

# Base directories where the folders are located
base_directories = [f"D:\\AI internship\\Collated Image Test\\Lusaran V1 110 DAFI\\T1\\mango00{i}" for i in range(2, 3)]

# Iterate through the base directories
for base_directory in base_directories:
    # Iterate through the folder structure
    for folder in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder)
        if os.path.isdir(folder_path):
            images = sorted(os.listdir(folder_path))
            if len(images) == 3:  # Assuming exactly 3 images in each folder
                # Swap the names of the first and third image using a temporary name
                first_image = images[0]
                third_image = images[2]
                temp_image_name = "temp_image.tmp"

                first_image_path = os.path.join(folder_path, first_image)
                third_image_path = os.path.join(folder_path, third_image)
                temp_image_path = os.path.join(folder_path, temp_image_name)

                # Step 1: Rename first image to temporary name
                os.rename(first_image_path, temp_image_path)
                # Step 2: Rename third image to first image's original name
                os.rename(third_image_path, first_image_path)
                # Step 3: Rename temporary name to third image's original name
                os.rename(temp_image_path, third_image_path)

                print(f"Swapped names of '{first_image}' and '{third_image}'")
            else:
                print(f"Expected exactly 3 images in {folder}, but found {len(images)}. Skipping folder.")
        else:
            print(f"Skipping non-directory file: {folder}")
