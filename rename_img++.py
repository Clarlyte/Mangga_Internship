import os
import pandas as pd

# Define the file path to your Excel file
excel_file_path = r"D:\AI Internship Repo\Mangga PNLS Classification.xlsx"
base_directory = r"D:\AI Internship Repo\Test"

# Load all sheets from the Excel file into a single DataFrame with an additional column for sheet names
all_sheets = pd.read_excel(excel_file_path, sheet_name=None)
data_frames = []
for sheet_name, df in all_sheets.items():
    df['SheetName'] = sheet_name
    data_frames.append(df)
combined_df = pd.concat(data_frames)

# Mapping full names to single-letter abbreviations
rating_map = {
    'Local': 'L',
    'Export': 'E',
    'Reject': 'R'
}

# Set to keep track of processed files to prevent re-processing
processed_files = set()

# Function to rename images based on ratings
def process_images(df, base_directory):
    for index, row in df.iterrows():
        mango_id = str(row['MangoID']).strip()

        # Traverse the directory to find matching files
        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if mango_id in file[:-4] and file not in processed_files:  # Check if file has not been processed
                    new_base_name = file[:-4]  # Base name without the extension

                    if 'S1' in file and 'SS' in file:
                        rating = rating_map.get(str(row['Side Rating']).strip(), 'Unknown')
                    elif 'S1' in file and 'TT' in file:
                        rating = rating_map.get(str(row['Top Rating']).strip(), 'Unknown')
                    elif 'S1' in file and 'BB' in file:
                        rating = rating_map.get(str(row['Bottom Rating']).strip(), 'Unknown')
                    else:
                        continue  # Skip if no valid orientation is found

                    new_name = f"{new_base_name}{rating}.{file.split('.')[-1]}"
                    os.rename(os.path.join(root, file), os.path.join(root, new_name))
                    print(f"Renamed '{file}' to '{new_name}'")
                    processed_files.add(new_name)  # Mark this new name as processed

# Process images for each sheet in the combined DataFrame
process_images(combined_df, base_directory)
