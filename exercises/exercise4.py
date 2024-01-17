import zipfile
import urllib.request
import pandas as pd
from sqlalchemy import BIGINT, TEXT, FLOAT

# 1: Download and unzip data
zip = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
zip_path = "mowesta-dataset.zip"
filename = "data.csv"

urllib.request.urlretrieve(zip, zip_path)
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extract(filename)

# 2: Reshape data
#Only use columns
columns = ["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"]
#Rename column names
new_cols = {"Temperatur in °C (DWD)": "Temperatur", "Batterietemperatur in °C": "Batterietemperatur"}

df = pd.read_csv(filename, delimiter=';', index_col=False, usecols=columns)
df.rename(columns=new_cols, inplace=True)

# 3: Transform data
df['Temperatur'] = df['Temperatur'].str.replace(',', '.').astype(float).apply(lambda x: (x * 9/5) + 32)
df['Batterietemperatur'] = df['Batterietemperatur'].str.replace(',', '.').astype(float).apply(lambda x: (x * 9/5) + 32)


# 4: Validate data
# Data Type Validation
df = df.astype({    "Geraet": int, "Monat": int, "Geraet aktiv": str })

# Fahrenheit Temperature Validation
valid_temp_range = (-459.67, 212)
temp_valid = df["Temperatur"].between(*valid_temp_range)
df = df[temp_valid]

# Batterietemperatur Validation
valid_battery_rang = df["Batterietemperatur"].between(*valid_temp_range)
df = df[valid_battery_rang]

# 5: Use fitting SQLite types & Write data into SQLite database
df.to_sql('temperatures', 'sqlite:///temperatures.sqlite', if_exists='replace', index=False, dtype={
        'Geraet': BIGINT,
        'Hersteller': TEXT,
        'Model': TEXT,
        'Monat': BIGINT,
        'Temperatur': FLOAT,
        'Batterietemperatur': FLOAT,
        'Geraet aktiv': TEXT
    })