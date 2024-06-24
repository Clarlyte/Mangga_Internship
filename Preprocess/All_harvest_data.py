import pandas as pd

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
