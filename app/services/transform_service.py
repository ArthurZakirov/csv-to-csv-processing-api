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
    df["processed"] = True
    return df
