import os
import pandas as pd

# Define the file path to your Excel file
excel_file_path = r"D:\AI internship\Without Local(E).xlsx"
base_directory = r"D:\AI internship\BG Removed - Copy"

# Load the Excel file
df = pd.read_excel(excel_file_path)

# Mapping full names to single-letter abbreviations
rating_map = {
    'Local': 'LO',
    'Export': 'EX',
    'Reject': 'RE',
    'X': 'NA'
}

# Set to keep track of processed files to prevent re-processing
processed_files = set()

# Function to rename images based on ratings
def process_images(df, base_directory):
    for index, row in df.iterrows():
        mango_id = str(row['MangoID']).strip()
        orientation = row['Orientation']
        bottom_rating = rating_map.get(str(row['Bottom Rating']).strip(), 'Unknown')
        side_rating = rating_map.get(str(row['Side Rating']).strip(), 'Unknown')
        top_rating = rating_map.get(str(row['Top Rating']).strip(), 'Unknown')

        # Define the orientation folder based on the Orientation number
        orientation_folder = f"S{orientation}"

        # Traverse the directory to find matching files
        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if mango_id in file[:-4] and file not in processed_files:  # Check if file has not been processed
                    new_base_name = file[:-4]  # Base name without the extension

                    if orientation_folder in file:
                        if 'SS' in file:
                            new_name = f"{new_base_name}{side_rating}.{file.split('.')[-1]}"
                        elif 'TT' in file:
                            new_name = f"{new_base_name}{top_rating}.{file.split('.')[-1]}"
                        elif 'BB' in file:
                            new_name = f"{new_base_name}{bottom_rating}.{file.split('.')[-1]}"
                        else:
                            continue  # Skip if no valid orientation is found

                        os.rename(os.path.join(root, file), os.path.join(root, new_name))
                        print(f"Renamed '{file}' to '{new_name}'")
                        processed_files.add(new_name)  # Mark this new name as processed

# Process images for each row in the DataFrame
process_images(df, base_directory)
