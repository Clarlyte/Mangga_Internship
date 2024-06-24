import pandas as pd
import os

# Define the file path to your Excel file
excel_file_path = r"D:\AI internship\Main\Mangga_Internship\Data Preparation.xlsx"
output_csv_file = 'collated_mango_data.csv'

# Mappings for site locations, mango locations, and elevation
site_location_map = {
    'ADLAON': 'AL', 'GUBA': 'GB', 'TABUELAN': 'TB', 'BOGO': 'BG', 'LUSARAN': 'LS'
}
mango_location_map = {
    'INSIDE': 'IN', 'OUT': 'OT', 'TOP': 'TP'
}
elevation_map = {
    'UPLAND': 'UP', 'LOWLAND': 'LW'
}

def create_unique_id(row):
    site_location = row['Site'].upper().strip()
    elevation = row['Elevation'].upper().strip()
    dafi = int(round(row['DAFI']))
    tree_info = row['TreeInfo'].split()
    tree_num = tree_info[0].upper().zfill(2)
    mango_loc = tree_info[1].upper()
    mango_num = str(row['MangoNum']).upper().zfill(2)
    flotation = row['Flotation'][0].upper() if pd.notnull(row['Flotation']) else 'X'

    site_abbr = site_location_map.get(site_location, 'Unknown')
    mango_loc_abbr = mango_location_map.get(mango_loc, 'Unknown')
    elevation_abbr = elevation_map.get(elevation, 'Unknown')

    return f"{site_abbr}{elevation_abbr}{dafi}{tree_num}M{mango_num}{mango_loc_abbr}{flotation}"

try:
    sheets = pd.read_excel(excel_file_path, sheet_name=None)
    all_data = pd.DataFrame()

    for sheet_name, df in sheets.items():
        df.columns = ['MangoNum', 'TreeInfo', 'Weight', 'Flotation', 'Size', 'Category', 'Site', 'DAFI', 'Elevation']
        df['UniqueID'] = df.apply(create_unique_id, axis=1)
        df[['Flotation', 'Size', 'Category']] = df[['Flotation', 'Size', 'Category']].applymap(lambda x: x[0] if pd.notnull(x) else x)
        all_data = pd.concat([all_data, df[['UniqueID', 'MangoNum', 'TreeInfo', 'Weight', 'Flotation', 'Size', 'Category']]], ignore_index=True)

    all_data.to_csv(output_csv_file, index=False)
    print(f"Collated data saved to '{output_csv_file}'")
except Exception as e:
    print(f"An error occurred: {e}")

# Base directory where the folders are located
base_directory = "D:\AI internship\Field Image Data raw - Copy (2)"


def get_tree_indicator(folder_name):
    tree_map = {
        0: 'T1',
        1: 'T2',
        2: 'T3',
        3: 'T4'
    }
    return tree_map.get(folder_name, 'Unknown')


# Function to map folder name to side indicator
def get_side_indicator(folder_name):
    side_map = {
        'side001': 'S1',
        'side002': 'S2',
        'side003': 'S3',
        'side004': 'S4'
    }
    return side_map.get(folder_name, 'Unknown')

# Function to get orientation indicator based on image order
def get_orientation_indicator(image_index):
    orientation_map = {
        0: 'T',
        1: 'S',
        2: 'B'
    }
    return orientation_map.get(image_index, 'Unknown')

# Iterate through the folder structure
for site_folder in os.listdir(base_directory):
    site_path = os.path.join(base_directory, site_folder)
    if os.path.isdir(site_path) and site_folder in sheets:
        df = sheets[site_folder]  # Ensure folder name matches sheet name exactly
        for tree_folder in os.listdir(site_path):
            tree_path = os.path.join(site_path, tree_folder)
            if os.path.isdir(tree_path):
                tree_info = tree_folder.split()[0]  # Extract the tree info from the folder name
                # Check if tree_info is in the DataFrame for this site
                if tree_info in df['TreeInfo'].astype(str).apply(lambda x: x.split()[0]).values:  # Ensure comparison as string
                    # Incorporate tree map here
                    tree_indicator = get_tree_indicator(tree_info)  # Assuming get_tree_indicator is adjusted to handle tree_info
                    for mango_folder in os.listdir(tree_path):
                        mango_path = os.path.join(tree_path, mango_folder)
                        if os.path.isdir(mango_path):
                            mango_num = (str(''.join(filter(str.isdigit, mango_folder))).lstrip('0'))
                            # Check if mango_num is in the DataFrame for this site and tree
                            if mango_num in df.loc[df['TreeInfo'].astype(str).apply(lambda x: x.split()[0]) == tree_info, 'MangoNum'].astype(str).values:  # Ensure comparison as string
                                for side_folder in os.listdir(mango_path):
                                    side_path = os.path.join(mango_path, side_folder)
                                    if os.path.isdir(side_path):
                                        side_indicator = get_side_indicator(side_folder)
                                        images = sorted(os.listdir(side_path))
                                        for index, image in enumerate(images):
                                            orientation_indicator = get_orientation_indicator(index)
                                            # Get the unique ID for the corresponding mango number
                                            unique_id = df.loc[(df['TreeInfo'].astype(str).apply(lambda x: x.split()[0]) == tree_info) & (df['MangoNum'].astype(str) == mango_num), 'UniqueID'].values[0]
                                            # Include tree_indicator in the new image name
                                            new_image_name = f"{unique_id}{side_indicator}{orientation_indicator}{orientation_indicator}.{image.split('.')[-1]}"
                                            os.rename(os.path.join(side_path, image), os.path.join(side_path, new_image_name))
                                            print(f"Renamed '{image}' to '{new_image_name}'")
                            else:
                                print(f"Mango number {mango_num} does not match any row in the sheets for {site_folder} and {tree_folder}, proceeding to the next mango folder.")
                else:
                    print(f"Tree info {tree_info} does not match any row in the sheets for {site_folder}, proceeding to the next tree folder.")
            else:
                print(f"Skipping non-directory file: {tree_folder}")
    else:
        print(f"Skipping non-directory file: {site_folder}")

    
        
