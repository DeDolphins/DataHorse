import pandas as pd
import glob

def save_uploaded_file(uploaded_file):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    df = load_dataframe()

    
    return df

def load_dataframe():

  all_files_csv = glob.glob("*.csv")
  for filename in all_files_csv:
      df = pd.read_csv(filename)
  return df