from sqlalchemy import create_engine
import pandas as pd

# Reading data from CSV file

data_url = 'https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV'

data_df = pd.read_csv(data_url, sep=';', decimal=',')

# --------  Dropping the Column (Status) --------

data_df = data_df.drop(['Status'], axis=1)

# -------- Dropping rows with Invalid entries --------

valid_verkehr = ["FV", "RV", "nur DPN"]

data_df = data_df[data_df['Verkehr'].isin(valid_verkehr)]

data_df = data_df[(data_df['Laenge'] >= -90) & (data_df['Laenge'] <= 90) & (data_df['Breite'] >= -90) & (data_df['Breite'] <= 90)]

data_df = data_df[data_df['IFOPT'].str.contains(r'^[A-Za-z]{2}:\d*:\d*(?::\d*)?$', na=False)]

data_df = data_df.dropna()

# -------- Conversion of Column (Betreiber_Nr) to integer --------

data_df["Betreiber_Nr"] = data_df["Betreiber_Nr"].astype(int)

# -------- Creating the engine without printing the execution details --------

engine = create_engine("sqlite:///trainstops.sqlite", echo=False)

data_df.to_sql('trainstops', engine, if_exists='replace', index=False)