import os
import sys
from config.env_config import setup_env
from src.extract.unclean_data import unclean_data
from src.extract.extract import extract_data
from src.transform.transform import transform_data
from src.load.load import load_into_database
def main():
    try:
        
        # Get the argument from the run_etl command and set up the environment
        setup_env(sys.argv)
        print(
            f"ETL pipeline run successfully in "
            f"{os.getenv('ENV', 'error')} environment!"
        )
        uncleaned_data = unclean_data()
        print(uncleaned_data)
        extracted_data = extract_data()
        print("Extracting")
        print(extracted_data)
        transformed_data = transform_data(extracted_data)
        print(f"Data transformation is completed")
        print(transformed_data)
        print("Commencing Loading into the database")
        loading_data = load_into_database(transformed_data)
        print(loading_data)
    except Exception as e:
        print(f"Error has occurred: {e}")
    
    
    

if __name__ == "__main__":
    main()
