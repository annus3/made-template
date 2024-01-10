import os
import pandas as pd
import tempfile
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
from sqlalchemy import Table, Column, create_engine, MetaData, TEXT, INTEGER, FLOAT, inspect
import sqlite3

class DataPipeline:
    def __init__(self, table, database):
        self.table = table
        self.database = database
        self.engine = None

    @staticmethod
    def download_data(dataset):
        # Downloading data from Kaggle
        api = KaggleApi()
        api.authenticate()

        with tempfile.TemporaryDirectory() as tempdir:
            api.dataset_download_files(dataset, path=tempdir, unzip=False)
            zip_filepath = os.path.join(tempdir, dataset.split('/')[-1] + '.zip')

            with zipfile.ZipFile(zip_filepath, 'r') as zfile:
                csv_filename = [f for f in zfile.namelist() if f.endswith('.csv')][0]
                with zfile.open(csv_filename) as file:
                    df = pd.read_csv(file)
                    print(f"Loaded {csv_filename} into DataFrame.")

        return df

    @staticmethod
    def transform_dataframe(df):
        # Handling missing values in dataframe
        numerical_columns = df.select_dtypes(include=['number']).columns
        categorical_columns = df.select_dtypes(exclude=['number']).columns

        for col in numerical_columns:
            df[col].fillna(df[col].mean(), inplace=True)

        for col in categorical_columns:
            mode_value = df[col].mode()[0]
            df[col].fillna(mode_value, inplace=True)

        return df

    def establish_database_connection(self):
        # Create SQLite database file if it doesn't exist
        if not os.path.exists(self.database):
            conn = sqlite3.connect(self.database)
            conn.close()

        # Creating SQLite engine and defining tables
        self.engine = create_engine(f'sqlite:///{self.database}')
        metadata = MetaData()
        inspector = inspect(self.engine)

        if not inspector.has_table(self.table):
            if self.table == 'laliga':
                laliga = Table(self.table, metadata,
                               Column('Position', TEXT),
                               Column('Shirt number', INTEGER),
                               Column('Games played', INTEGER),
                               Column('Goal scored', INTEGER),
                               Column('Penalties scored', INTEGER),
                               Column('Own goals', INTEGER),
                               Column('Goals scored with header', INTEGER),
                               Column('From inside the area', INTEGER),
                               Column('From outside the area', INTEGER),
                               Column('Goals with left foot', INTEGER))
                metadata.create_all(self.engine)
            elif self.table == 'premier_league':
                premier_league = Table(self.table, metadata,
                                       Column('Position', TEXT),
                                       Column('Jersey Number', INTEGER),
                                       Column('Appearances', FLOAT),
                                       Column('Headed goals', INTEGER),
                                       Column('Goals', INTEGER),
                                       Column('Penalties Scored', INTEGER),
                                       Column('Own goals', INTEGER),
                                       Column('From Inside the area', INTEGER),
                                       Column('From outside the area', INTEGER),
                                       Column('Goals with left foot', INTEGER),
                                       Column('Freekicks scored', INTEGER),
                                       Column('Goals with right foot', INTEGER))
                metadata.create_all(self.engine)

    def load_data(self, df):
        # Loading data into SQLite tables
        self.engine.execute(f"DROP TABLE IF EXISTS {self.table};")
        df.to_sql(self.table, self.engine, if_exists='replace', index=False)

    def print_table_columns(self):
        # Displaying table columns
        if self.table == 'laliga':
            laliga_columns = [
                'Position', 'Shirt number', 'Games played', 'Goal scored', 'Penalties scored',
                'Own goals', 'Goals scored with header', 'From inside the area', 'From outside the area',
                'Goals with left foot'
            ]
            print(f"Columns in 'laliga' table: {laliga_columns}")
        elif self.table == 'premier_league':
            premier_columns = [
                'Position', 'Jersey Number', 'Appearances', 'Headed goals', 'Goals', 'Penalties Scored',
                'Own goals', 'From Inside the area', 'From outside the area', 'Goals with left foot',
                'Freekicks scored', 'Goals with right foot'
            ]
            print(f"Columns in 'premier_league' table: {premier_columns}")

    def run_pipeline(self):
        # Running the data pipeline
        if self.table == 'laliga':
            data = self.download_data('thegreatcoder/laliga-player-stats')
        elif self.table == 'premier_league':
            data = self.download_data('rishikeshkanabar/premier-league-player-statistics-updated-daily')
        else:
            raise ValueError(f"No dataset URL provided for table: {self.table}")

        if data is not None:
            transformed_data = self.transform_dataframe(data)
            self.establish_database_connection()
            self.load_data(transformed_data)
            print(f"ETL -- Successfully completed for {self.table}.")
        else:
            raise FileNotFoundError(f'Failed to load data for {self.table}. Check if correct data is provided.')

    def get_all_data_from_database(self):
        # Fetching dataframes from database
        with self.engine.connect() as connection:
            query = f"SELECT * FROM {self.table};"
            dataframe = pd.read_sql_query(query, connection)
        return dataframe

def main():
    # Driver code to run the pipeline for 'laliga' and 'premier_league' tables
    _database = '../data/data.sqlite'

    laliga_table = 'laliga'
    premier_table = 'premier_league'

    laliga_pipeline = DataPipeline(table=laliga_table, database=_database)
    #laliga_pipeline.print_table_columns()
    laliga_pipeline.run_pipeline()
    laliga_df = laliga_pipeline.get_all_data_from_database()

    premier_pipeline = DataPipeline(table=premier_table, database=_database)
    #premier_pipeline.print_table_columns()
    premier_pipeline.run_pipeline()
    premier_table_df = premier_pipeline.get_all_data_from_database()
    
    # data_frame1 = download_data(dataset1)
    # data_frame2 = download_data(dataset2)
    # processed_df1 = transform_dataframe(data_frame1)
    # processed_df2 = transform_dataframe(data_frame2)

    
if __name__ == "__main__":
    main()
