import os
import json
import requests
import pandas as pd
from datetime import datetime
from google.cloud import storage

CONFIG_PATH = "./tmp/config_file.json"

def get_config_data():
    """
        Function to read and parse the config data from a JSON file

        returns: dictionary of config data
    """
    try:
        # Open and read the JSON file
        with open(CONFIG_PATH, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error reading config data: {e}")


# setup key variables
config_data = get_config_data()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=config_data['credential_path']
project_id = config_data['project_id']
storage_client = storage.Client(project_id)
URL = config_data['poke_url']


# define extract, transform, load functions
def api_request():
    """
        Function to request pokemon information and select pokemon name, weight, height, base experience,
        ability names and image sprite for 10 pokemons 

        returns: list of pokemon dictionary data
    """
    try:
        # set list of results
        results = []
        # loop through and collected 10 api requests
        for i in range(1, 11):
            response = requests.get(URL + str(i))
            if response.status_code == 200:
                json = response.json()
                data = {}
                data['name'] = json['name']
                data['weight'] = json['weight']
                data['height'] = json['height']
                data['base_experience'] = json['base_experience']
                
                # get list of ability names and add to data dictionary
                abilities = []
                for ability in json['abilities']:
                    abilities.append(ability['ability']['name'])
                data['abilities'] = abilities
                data['sprite'] = json['sprites']['front_default']

                results.append(data)
            else:
                print(f"Error fetching data for pokemon {i}. Status code: {response.status_code}")
       # return pokemon data collected
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")


def transform(data):
    """
        Function to transform and capitalise string data 
        returns: transformed data as list of data dictionaries
    """
    try:
        # capitalise names and ability names
        for pokemon in data:
            pokemon['name'] = pokemon['name'].capitalize()
            # remoeve - from ability, then capitlise and convert abilities to a string
            pokemon['abilities'] = ', '.join([ability.replace('-', ' ').capitalize() for ability in pokemon['abilities']])

        return data
    except Exception as e:
            print(f"Error during transformation: {e}")


def load_data(data):
    """
        Function to load data into GCP Cloud as a csv
        returns: None
    """
    try:
        # load data to GCP bucket
        bucket_name = config_data['bucket_name']
        folder_prefix = config_data['bucket_folder_prefix']
        # here you would use the GCP client to upload the data to the bucket
        df = pd.DataFrame(data)
        new_save_location = f"gs://{bucket_name}/{folder_prefix}/pokemon_data.csv"
        df.to_csv(new_save_location, index=False)

        print('Data loaded successfully to GCP bucket')

    except Exception as e:
        print(f"Error during loading data: {e}")


def logging(process):
    """
        Function to log process execution
        returns: None
    """
    try:
        datetimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Logging process: {process} completed at {datetimestamp}')

    except Exception as e:
        print(f"Error during logging: {e}")


# run function defined
def run():
    """ 
        Main function to run the ETL application
        returns: None
    """
    # get data from API
    data = api_request()
    logging('Data extraction')
    
    # transform data
    tranformed_data = transform(data)
    logging('Data transformation')
    
    # load data to GCP bucket
    load_data(tranformed_data)
    logging('Data load')


# output results to GCP bucket
print('Start Pokemon Data ETL...')
run()
print('Completed Pokemon Data ETL to GCP')