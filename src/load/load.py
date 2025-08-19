import os 
import pandas as pd
import timeit 
import psycopg2
from config.db_config import load_db_config
from sqlalchemy import create_engine

def load_into_database(tracks: pd.DataFrame):
    start_time = timeit.default_timer()
    
    try:
        # Load config to get connection details
        connection_details = load_db_config()["source_database"]
        connection = psycopg2.connect(
            dbname=connection_details["dbname"],
            user=connection_details["user"],
            password=connection_details["password"],
            host=connection_details["host"],
            port=connection_details["port"]       
        )
        # Read SQL query
        CREATE_TABLE_QUERY_FILE = os.path.join(
            os.path.dirname(__file__),
            r"C:\Users\ruben\OneDrive\Desktop\digitalfutures\Capstone-Project\src\sql\create_table.sql"
        )
        with open(CREATE_TABLE_QUERY_FILE, "r") as file:
            query = file.read()
        # Create table in database
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        
        engine = create_engine(
            f"postgresql+psycopg2://{connection_details['user']}:{connection_details['password']}@"
            f"{connection_details['host']}:{connection_details['port']}/{connection_details['dbname']}"
        )
        # Add data to the database
        tracks.to_sql(
            'ruben_capstone',
            con=engine,
            schema='de_2506_a',
            if_exists='append',
            index=False
        )
        print("Data loaded into the database")
        connection.close()
        cursor.close()
    except Exception as e:
        print(f"An Error has occurred during the loading phase: {e}")
            
        