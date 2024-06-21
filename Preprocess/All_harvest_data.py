import pandas as pd

# Define the file path to your Excel file
excel_file = r"D:\AI internship\Data Preparation.xlsx"

# Mappings for site locations, mango locations, and elevation
site_location_map = {
    'ADLAON': 'AL',
    'GUBA': 'GB',
    'TABUELAN': 'TB',
    'BOGO': 'BG',
    'LUSARAN': 'LS'
}

mango_location_map = {
    'INSIDE': 'IN',
    'OUT': 'OT',
    'TOP': 'TP'
}

elevation_map = {
    'UPLAND': 'UP',
    'LOWLAND': 'LW'
}

# Function to create UniqueID based on the convention
def create_unique_id(row):
    # Extract required fields from the row
    site_location = str(row['Site']).upper().strip()
    elevation = str(row['Elevation']).upper()
    dafi = int(round(float(row['DAFI'])))  # DAFI (rounded to the nearest integer
    tree_info = str(row['TreeInfo']).split()
    tree_num = tree_info[0].strip().upper().zfill(2)  # Tree number, padded with zero if necessary
    mango_loc = tree_info[1].upper()
    mango_num = str(row['MangoNum']).strip().upper().zfill(2)  # Mango number, padded with zero if necessary

        
    # Transform site location, mango location, and elevation using the mappings
    site_abbr = site_location_map.get(site_location[:7], 'Unknown')  # Adjusted to match the full name
    mango_loc_abbr = mango_location_map.get(mango_loc[:7], 'Unknown')  # Adjusted for full name
    elevation_abbr = elevation_map.get(elevation[:7], 'Unknown')  # Adjusted for full nam
    
    # Create the UniqueID
    unique_id = f"{site_abbr}{elevation_abbr}{dafi}{tree_num}M{mango_num}{mango_loc_abbr}"
    return unique_id

# Read all sheets from Excel file into a dictionary of DataFrames
sheets = pd.read_excel(excel_file, sheet_name=None)

# Initialize an empty DataFrame to hold all data
all_data = pd.DataFrame()

# Iterate through each sheet
for sheet_name, df in sheets.items():
    # Rename columns to ensure consistency
    df.columns = ['MangoNum', 'TreeInfo', 'Weight', 'Flotation', 'Size', 'Category', 'Site', 'DAFI', 'Elevation']
    
    # Create UniqueID column
    df['UniqueID'] = df.apply(create_unique_id, axis=1)
    
    # Extract the first letter for Flotation, Size, and Category columns
    for column in ['Flotation', 'Size', 'Category']:
        df[column] = df[column].apply(lambda x: x[0] if pd.notnull(x) else x)
    
    # Append only the necessary columns and the UniqueID to the all_data DataFrame
    all_data = pd.concat([all_data, df[['UniqueID', 'MangoNum', 'TreeInfo', 'Weight', 'Flotation', 'Size', 'Category']]], ignore_index=True)

# Save the collated data to a CSV file
output_csv = 'collated_mango_data.csv'
all_data.to_csv(output_csv, index=False)

print(f"Collated data saved to '{output_csv}'")
