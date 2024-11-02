import pandas as pd
import re
from io import StringIO

def process_csv(input_data: bytes) -> str:
    # Read CSV file into a DataFrame
    df = pd.read_csv(StringIO(input_data.decode("utf-8")))
    
    # Process the DataFrame
    df = process_dataframe(df)
    
    # Convert the DataFrame back to a CSV string
    output_csv = df.to_csv(index=False)
    return output_csv

def process_dataframe(df):
    # 1. Remove duplicates based on ID column
    df = df.drop_duplicates(subset=[df.columns[0]])  # Assume first column is ID

    # 2. Standardize capitalization in object (string) columns
    df = df.apply(lambda x: x.str.title() if x.dtype == "object" else x)

    # 3. Remove extra spaces and any quotes around values in object columns
    df = df.apply(lambda x: x.str.strip(' "\'') if x.dtype == "object" else x)

    # 4. Selectively convert strings that represent numerical data to integers
    def try_convert_column_to_int(series):
        def clean_and_convert(value):
            if isinstance(value, str):
                cleaned = re.sub(r'\D', '', value)
                return int(cleaned) if cleaned else None
            return value

        try:
            series_cleaned = series.apply(clean_and_convert)
            if pd.api.types.is_numeric_dtype(series_cleaned.dropna()):
                return series_cleaned
        except:
            pass
        return series

    df = df.apply(lambda col: try_convert_column_to_int(col) if col.dtype == "object" else col)

    # 5. Convert binary categorical columns to boolean
    for col in df.select_dtypes(include="object").columns:
        unique_values = df[col].dropna().unique()
        if len(unique_values) == 2:
            val_1, val_0 = unique_values[0], unique_values[1]
            df[col] = df[col].map({val_1: 1, val_0: 0})
            new_col_name = f"{col}_{val_1}"
            df.rename(columns={col: new_col_name}, inplace=True)

    return df