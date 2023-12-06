import sqlite3
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
import os
import zipfile
import tempfile
import requests
import io

def download_data_from_kaggle(dataset):
    api = KaggleApi()
    api.authenticate()

    with tempfile.TemporaryDirectory() as tempdir:
        api.dataset_download_files(dataset, path=tempdir, unzip=False)

        zip_filepath = os.path.join(tempdir, dataset.split('/')[-1] + '.zip')

        data_frames = []
        with zipfile.ZipFile(zip_filepath, 'r') as zfile:
            for filename in zfile.namelist():
                with zfile.open(filename) as file:
                    if filename.endswith('.csv'):
                        df = pd.read_csv(file)
                        data_frames.append(df)
                        print(f"Loaded {filename} into DataFrame.")

    return data_frames

def main():
    api = KaggleApi()
    api.authenticate()

    dataset1 = 'thegreatcoder/laliga-player-stats'
    dataset2 = 'rishikeshkanabar/premier-league-player-statistics-updated-daily'

    
    data_frames1 = download_data_from_kaggle(dataset1)
    data_frames2 = download_data_from_kaggle(dataset2)

    conn = sqlite3.connect('my_database.db')
    cur = conn.cursor()

  
    for df in data_frames1:
        df.to_sql('Players_Table', conn, if_exists='append', index=False)

    for df in data_frames2:
        df.to_sql('Player_Feature', conn, if_exists='replace', index=False)

    
    response1 = requests.get('https://www.kaggle.com/datasets/rishikeshkanabar/premier-league-player-statistics-updated-daily/download?datasetVersionNumber=2')
    data_1 = response1.json()


    cur.execute('''
        CREATE TABLE IF NOT EXISTS Players_Table (
            PlayerPosition TEXT,
            GoalScored INTEGER
        )
    ''')

    
    for entry in data_frames2[0].to_dict(orient='records'):
        cur.execute('''
            INSERT INTO Players_Table (PlayerPosition, GoalScored)
            VALUES (?, ?)
        ''', (entry['PlayerPosition'], entry['GoalScored']))

    
    data_2 = data_frames1[0]  

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Player_Features (
            NoOfGames Integer,
            MinutesPlayed INTEGER
        )
    ''')

    data_2.to_sql('Player_Features', conn, if_exists='replace', index=False)

    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
