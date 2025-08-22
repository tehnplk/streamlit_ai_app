import pandas as pd
from io import StringIO

def convert_csv_to_tabular(csv_data: str) -> str:
    df = pd.read_csv(StringIO(csv_data))
    return df.to_markdown(index=False)
  