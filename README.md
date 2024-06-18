# Project Mangga

Project Mangga is a data processing and analysis project focused on the maturity of mangoes harvested from various highland and lowland locations. The project includes a script that standardizes, collates, and uniquely identifies data from multiple Excel sheets into a single CSV file, ensuring consistent and organized data for further analysis.

## Features
- **Standardizes Column Names**: Handles variations in column names across different sheets.
- **Unique Identifier Generation**: Creates a unique ID for each row based on location, elevation, harvest date, and test result, ensuring no duplicates.
- **Data Collation**: Merges data from multiple sheets into one cohesive CSV file.

## Usage
1. Place your Excel file with multiple sheets in the project directory.
2. Run the provided Python script to process the data.
3. The script will output a CSV file with collated and uniquely identified data.

## Requirements
- Python 3.x
- pandas library

## Installation
Install the pandas library using pip:
```bash
pip install pandas
```

## Running the Script
Execute the script with your Excel file:
```bash
python process_mango_data.py
```

## Output
The script generates a CSV file named `collated_mango_data.csv` containing the processed data.


